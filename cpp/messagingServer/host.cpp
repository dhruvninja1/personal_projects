#include <iostream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <fcntl.h>
#include <sys/event.h>
#include <cerrno>
#include <algorithm>
#include <map>

using namespace std;

void broadcast_message(const string& message, int sender_fd = -1);
bool set_non_blocking(int fd);
void remove_client(int fd);

vector<int> client_sockets;
string SERVER_PASSWORD;
map<int, bool> authenticated_clients; // To track authenticated clients
map<int, string> client_usernames;    // To track client usernames
map<int, int> client_auth_stage;      // 0 = password needed, 1 = username needed, 2 = fully authenticated

bool set_non_blocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return false;
    flags |= O_NONBLOCK;
    return fcntl(fd, F_SETFL, flags) != -1;
}

void remove_client(int fd) {
    // Broadcast leave message if client was authenticated
    if (authenticated_clients.count(fd) && authenticated_clients[fd]) {
        if (client_usernames.count(fd)) {
            string leave_message = client_usernames[fd] + " has left the chat!";
            broadcast_message(leave_message, fd);
        }
    }
    
    auto it = find(client_sockets.begin(), client_sockets.end(), fd);
    if (it != client_sockets.end()) {
        client_sockets.erase(it);
    }
    authenticated_clients.erase(fd);
    client_usernames.erase(fd);
    client_auth_stage.erase(fd);
    close(fd);
}

void broadcast_message(const string& message, int sender_fd) {
    for (int client_fd : client_sockets) {
        if (client_fd != sender_fd) {
            ssize_t bytes_sent = send(client_fd, message.c_str(), message.length(), 0);
            if (bytes_sent == -1) {
                if (errno != EWOULDBLOCK && errno != EAGAIN) {
                    cerr << "Error: Failed to send message to client " << client_fd << ". Closing socket." << endl;
                    remove_client(client_fd);
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: ./host <port> <password>" << endl;
        exit(1);
    }
    const int PORT = stoi(argv[1]);
    SERVER_PASSWORD = argv[2];

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        cerr << "Error: Failed to create socket." << endl;
        return 1;
    }

    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        cerr << "Error: setsockopt failed." << endl;
        return 1;
    }

    sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if (::bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Error: Failed to bind socket." << endl;
        close(server_fd);
        return 1;
    }

    if (listen(server_fd, 5) < 0) {
        cerr << "Error: Failed to listen on socket." << endl;
        close(server_fd);
        return 1;
    }
    
    set_non_blocking(server_fd);

    int kq_fd = kqueue();
    if (kq_fd == -1) {
        cerr << "Error: kqueue failed." << endl;
        return 1;
    }

    struct kevent change_event;
    EV_SET(&change_event, server_fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
    kevent(kq_fd, &change_event, 1, NULL, 0, NULL);

    const int MAX_EVENTS = 128;
    struct kevent event_list[MAX_EVENTS];

    while (true) {
        int num_events = kevent(kq_fd, NULL, 0, event_list, MAX_EVENTS, NULL);
        if (num_events < 0) {
            cerr << "Error: kevent failed in event loop." << endl;
            continue;
        }

        for (int i = 0; i < num_events; ++i) {
            int event_fd = event_list[i].ident;

            if (event_list[i].flags & EV_ERROR || event_list[i].flags & EV_EOF) {
                remove_client(event_fd);
                continue;
            }

            if (event_fd == server_fd) {
                sockaddr_in client_addr;
                socklen_t client_addr_len = sizeof(client_addr);
                int client_socket = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
                if (client_socket == -1) continue;
                
                set_non_blocking(client_socket);

                // Add the new client to the map as unauthenticated
                authenticated_clients[client_socket] = false;
                client_auth_stage[client_socket] = 0; // Expecting password first

                EV_SET(&change_event, client_socket, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
                kevent(kq_fd, &change_event, 1, NULL, 0, NULL);
            } else {
                char buffer[1024];
                ssize_t bytes_read = recv(event_fd, buffer, sizeof(buffer), 0);
                
                if (bytes_read > 0) {
                    string received_message(buffer, bytes_read);

                    if (authenticated_clients.at(event_fd)) {
                        // Fully authenticated, broadcast the regular message
                        broadcast_message(received_message, event_fd);
                    } else {
                        // Handle authentication stages
                        int stage = client_auth_stage[event_fd];
                        
                        if (stage == 0) {
                            // Expecting password
                            if (received_message == SERVER_PASSWORD) {
                                client_auth_stage[event_fd] = 1; // Move to username stage
                                send(event_fd, "PASSWORD_OK", 11, 0);
                                cout << "Client " << event_fd << " password authenticated. Waiting for username." << endl;
                            } else {
                                send(event_fd, "FAIL", 4, 0);
                                remove_client(event_fd);
                            }
                        } else if (stage == 1) {
                            // Expecting username
                            string username = received_message;
                            client_usernames[event_fd] = username;
                            authenticated_clients[event_fd] = true;
                            client_auth_stage[event_fd] = 2;
                            client_sockets.push_back(event_fd);
                            
                            send(event_fd, "OK", 2, 0);
                            
                            // Broadcast join message
                            string join_message = username + " has joined the chat!";
                            broadcast_message(join_message, event_fd);
                            cout << "User '" << username << "' (client " << event_fd << ") has joined the chat." << endl;
                        }
                    }
                } else if (bytes_read == 0) {
                    remove_client(event_fd);
                } else if (errno != EWOULDBLOCK && errno != EAGAIN) {
                    remove_client(event_fd);
                }
            }
        }
    }
    return 0;
}