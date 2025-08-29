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
#include <sstream>

using namespace std;

void broadcast_message(const string& message, int sender_fd = -1);
bool set_non_blocking(int fd);
void remove_client(int fd);
void handle_admin_command(const string& message, int admin_fd);
string encrypt_message(const string& message, const string& key);
string decrypt_message(const string& encrypted, const string& key);

vector<int> client_sockets;
string SERVER_PASSWORD;
string ADMIN_PASSWORD;
map<int, bool> authenticated_clients; // To track authenticated clients
map<int, string> client_usernames;    // To track client usernames
map<int, int> client_auth_stage;      // 0 = password needed, 1 = username needed, 2 = fully authenticated
map<int, bool> admin_clients;         // To track admin clients
map<int, bool> muted_clients;         // To track muted clients

// XOR encryption using admin password as key
string encrypt_message(const string& message, const string& key) {
    string encrypted = message;
    for (size_t i = 0; i < message.length(); ++i) {
        encrypted[i] = message[i] ^ key[i % key.length()];
    }
    return encrypted;
}

string decrypt_message(const string& encrypted, const string& key) {
    // XOR is symmetric, so decryption is the same as encryption
    return encrypt_message(encrypted, key);
}

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
    admin_clients.erase(fd);
    muted_clients.erase(fd);
    close(fd);
}

void broadcast_message(const string& message, int sender_fd) {
    // Encrypt the message before broadcasting
    string encrypted_message = encrypt_message(message, ADMIN_PASSWORD);
    
    for (int client_fd : client_sockets) {
        if (client_fd != sender_fd) {
            ssize_t bytes_sent = send(client_fd, encrypted_message.c_str(), encrypted_message.length(), 0);
            if (bytes_sent == -1) {
                if (errno != EWOULDBLOCK && errno != EAGAIN) {
                    cerr << "Error: Failed to send message to client " << client_fd << ". Closing socket." << endl;
                    remove_client(client_fd);
                }
            }
        }
    }
}

int find_client_by_username(const string& username) {
    for (auto& pair : client_usernames) {
        if (pair.second == username) {
            return pair.first;
        }
    }
    return -1;
}

void handle_admin_command(const string& message, int admin_fd) {
    string admin_username = client_usernames[admin_fd];
    
    if (message.find("admin.mute ") == 0) {
        string target_username = message.substr(11); // Remove "admin.mute "
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            muted_clients[target_fd] = true;
            
            // Notify the target user they are muted (encrypt notification)
            string mute_notification = "ADMIN_MUTE:You have been muted by an administrator.";
            string encrypted_notification = encrypt_message(mute_notification, ADMIN_PASSWORD);
            send(target_fd, encrypted_notification.c_str(), encrypted_notification.length(), 0);
            
            // Broadcast mute message
            string mute_message = target_username + " has been muted by " + admin_username;
            broadcast_message(mute_message, admin_fd);
            
            cout << "Admin " << admin_username << " muted user " << target_username << endl;
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            string encrypted_error = encrypt_message(error_msg, ADMIN_PASSWORD);
            send(admin_fd, encrypted_error.c_str(), encrypted_error.length(), 0);
        }
    }
    else if (message.find("admin.kick ") == 0) {
        string target_username = message.substr(11); // Remove "admin.kick "
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            // Notify the target user they are being kicked (encrypt notification)
            string kick_notification = "ADMIN_KICK:You have been kicked by an administrator.";
            string encrypted_notification = encrypt_message(kick_notification, ADMIN_PASSWORD);
            send(target_fd, encrypted_notification.c_str(), encrypted_notification.length(), 0);
            
            // Broadcast kick message
            string kick_message = target_username + " has been kicked by " + admin_username;
            broadcast_message(kick_message, admin_fd);
            
            cout << "Admin " << admin_username << " kicked user " << target_username << endl;
            
            // Remove the client (this will also broadcast leave message)
            remove_client(target_fd);
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            string encrypted_error = encrypt_message(error_msg, ADMIN_PASSWORD);
            send(admin_fd, encrypted_error.c_str(), encrypted_error.length(), 0);
        }
    }
    else if (message.find("admin.unmute ") == 0) {
        string target_username = message.substr(13); // Remove "admin.unmute "
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            muted_clients[target_fd] = false;
            
            // Notify the target user they are unmuted (encrypt notification)
            string unmute_notification = "ADMIN_UNMUTE:You have been unmuted by an administrator.";
            string encrypted_notification = encrypt_message(unmute_notification, ADMIN_PASSWORD);
            send(target_fd, encrypted_notification.c_str(), encrypted_notification.length(), 0);
            
            // Broadcast unmute message
            string unmute_message = target_username + " has been unmuted by " + admin_username;
            broadcast_message(unmute_message, admin_fd);
            
            cout << "Admin " << admin_username << " unmuted user " << target_username << endl;
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            string encrypted_error = encrypt_message(error_msg, ADMIN_PASSWORD);
            send(admin_fd, encrypted_error.c_str(), encrypted_error.length(), 0);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Usage: ./host <port> <password> <admin_password>" << endl;
        exit(1);
    }
    const int PORT = stoi(argv[1]);
    SERVER_PASSWORD = argv[2];
    ADMIN_PASSWORD = argv[3];

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

    cout << "Server started on port " << PORT << endl;
    cout << "Regular password: " << SERVER_PASSWORD << endl;
    cout << "Admin password: " << ADMIN_PASSWORD << endl;
    cout << "Encryption enabled using admin password as key for all messages" << endl;

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
                admin_clients[client_socket] = false;
                muted_clients[client_socket] = false;

                EV_SET(&change_event, client_socket, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
                kevent(kq_fd, &change_event, 1, NULL, 0, NULL);
            } else {
                char buffer[1024];
                ssize_t bytes_read = recv(event_fd, buffer, sizeof(buffer), 0);
                
                if (bytes_read > 0) {
                    string received_message(buffer, bytes_read);

                    if (authenticated_clients.at(event_fd)) {
                        // Decrypt the received message
                        string decrypted_message = decrypt_message(received_message, ADMIN_PASSWORD);
                        
                        // Check if this is an admin command
                        if (admin_clients[event_fd] && decrypted_message.find("admin.") == 0) {
                            handle_admin_command(decrypted_message, event_fd);
                        } else {
                            // Check if user is muted
                            if (muted_clients[event_fd]) {
                                string mute_reminder = "MUTED:You are muted and cannot send messages.";
                                string encrypted_reminder = encrypt_message(mute_reminder, ADMIN_PASSWORD);
                                send(event_fd, encrypted_reminder.c_str(), encrypted_reminder.length(), 0);
                            } else {
                                // Fully authenticated and not muted, broadcast the decrypted message
                                broadcast_message(decrypted_message, event_fd);
                            }
                        }
                    } else {
                        // Handle authentication stages (these are not encrypted)
                        int stage = client_auth_stage[event_fd];
                        
                        if (stage == 0) {
                            // Expecting password
                            bool is_admin = false;
                            if (received_message == ADMIN_PASSWORD) {
                                is_admin = true;
                                admin_clients[event_fd] = true;
                            } else if (received_message != SERVER_PASSWORD) {
                                send(event_fd, "FAIL", 4, 0);
                                remove_client(event_fd);
                                continue;
                            }
                            
                            client_auth_stage[event_fd] = 1; // Move to username stage
                            
                            // Send response with encryption key
                            string response;
                            if (is_admin) {
                                response = "ADMIN_KEY:" + ADMIN_PASSWORD;
                            } else {
                                response = "KEY:" + ADMIN_PASSWORD;
                            }
                            send(event_fd, response.c_str(), response.length(), 0);
                            cout << "Client " << event_fd << (is_admin ? " (ADMIN)" : "") << " password authenticated. Encryption key sent. Waiting for username." << endl;
                        } else if (stage == 1) {
                            // Expecting username
                            string username = received_message;
                            if (admin_clients[event_fd]) {
                                username = "[ADMIN] " + username;
                            }
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