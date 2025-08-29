#define DEBUG 1

#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

using namespace std;

// ANSI color codes
const string COLOR_RESET = "\033[0m";
const string COLOR_CYAN = "\033[36m";
const string COLOR_GREEN = "\033[32m";
const string COLOR_YELLOW = "\033[33m";
const string COLOR_BLUE = "\033[34m";
const string COLOR_MAGENTA = "\033[35m";
const string COLOR_LIGHT_RED = "\033[91m";     // Light red for leave messages
const string COLOR_LIGHT_GREEN = "\033[92m";   // Light green for join messages

// emoji shi

// Function to handle sending and receiving messages after successful authentication.
void chat_with_server(int client_socket, const string& username) {
    string current_input;
    char buffer[1024] = {0};

    cout << "Authentication successful! You can now send messages." << endl;
    cout << "Type a message and press Enter. To exit, type 'cmd.exit'." << endl;
    cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << flush; // Initial prompt

    while (true) {
        fd_set read_fds;
        FD_ZERO(&read_fds);
        FD_SET(STDIN_FILENO, &read_fds);
        FD_SET(client_socket, &read_fds);

        if (select(client_socket + 1, &read_fds, NULL, NULL, NULL) < 0) {
            cerr << "Error with select()." << endl;
            break;
        }

        if (FD_ISSET(STDIN_FILENO, &read_fds)) {
            getline(cin, current_input);
            if (current_input == "cmd.exit") {
                break;
            }
            else if (current_input == "cmd.sybau"){
                current_input = "Sybau 💔🥀";
            }
            // Format message with username
            string formatted_message = username + " - " + current_input;
            send(client_socket, formatted_message.c_str(), formatted_message.length(), 0);
            cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << flush; // Show prompt for next message
        }

        if (FD_ISSET(client_socket, &read_fds)) {
            memset(buffer, 0, sizeof(buffer));
            ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
            if (bytes_received > 0) {
                string received_message(buffer, bytes_received);
                
                // Clear the current prompt line
                cout << "\r\033[K"; // Move to beginning of line and clear it
                
                // Check if it's a join/leave message
                if (received_message.find(" has joined the chat!") != string::npos) {
                    // Display join messages in light green
                    cout << COLOR_LIGHT_GREEN << received_message << COLOR_RESET << endl;
                } else if (received_message.find(" has left the chat!") != string::npos) {
                    // Display leave messages in light red
                    cout << COLOR_LIGHT_RED << received_message << COLOR_RESET << endl;
                } else {
                    // Find the dash separator to split username and message
                    size_t dash_pos = received_message.find(" - ");
                    if (dash_pos != string::npos) {
                        string sender_name = received_message.substr(0, dash_pos);
                        string actual_message = received_message.substr(dash_pos + 3);
                        cout << COLOR_CYAN << sender_name << COLOR_RESET << " - " << actual_message << endl;
                    } else {
                        // Fallback if message doesn't have expected format
                        cout << received_message << endl;
                    }
                }
                
                // Restore the prompt
                cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << flush;
            } else if (bytes_received == 0) {
                cout << "\r\033[K"; // Clear current line
                cout << "Server disconnected." << endl;
                break;
            } else {
                cerr << "Error receiving data." << endl;
                break;
            }
        }
    }
}

int main() {
    string host, password, username;
    int port;

    // 1. Get connection details from standard input
    cout << "Enter username: ";
    getline(cin, username);
    #ifndef DEBUG
    cout << "Enter hostname or IP: ";
    getline(cin, host);
    cout << "Enter port: ";
    cin >> port;
    cin.ignore(); // Clear the newline character from the buffer
    cout << "Enter password: ";
    getline(cin, password);

    #endif
    #ifdef DEBUG
    host = "localhost";
    port = 8080;
    password = "test";
    #endif

    // 2. Create the socket.
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        cerr << "Error creating socket." << endl;
        return 1;
    }

    // 3. Resolve the hostname.
    struct hostent* host_entry = gethostbyname(host.c_str());
    if (host_entry == nullptr) {
        cerr << "Error resolving hostname: " << host << endl;
        close(client_socket);
        return 1;
    }

    // 4. Prepare the server address structure.
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    memcpy(&server_addr.sin_addr, host_entry->h_addr_list[0], host_entry->h_length);

    // 5. Connect to the server.
    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Error connecting to server." << endl;
        close(client_socket);
        return 1;
    }

    cout << "Connected to server. Sending password..." << endl;

    // 6. Send the password for authentication.
    if (send(client_socket, password.c_str(), password.length(), 0) < 0) {
        cerr << "Error sending password." << endl;
        close(client_socket);
        return 1;
    }

    // 7. Wait for password authentication response.
    char auth_response[12] = {0};
    ssize_t bytes_received = recv(client_socket, auth_response, sizeof(auth_response) - 1, 0);
    if (bytes_received <= 0) {
        cerr << "Error receiving authentication response." << endl;
        close(client_socket);
        return 1;
    }

    string response(auth_response, bytes_received);
    if (response == "PASSWORD_OK") {
        cout << "Password accepted. Sending username..." << endl;
        
        // 8. Send the username
        if (send(client_socket, username.c_str(), username.length(), 0) < 0) {
            cerr << "Error sending username." << endl;
            close(client_socket);
            return 1;
        }
        
        // 9. Wait for final authentication response
        char final_response[3] = {0};
        bytes_received = recv(client_socket, final_response, sizeof(final_response) - 1, 0);
        if (bytes_received <= 0) {
            cerr << "Error receiving final authentication response." << endl;
            close(client_socket);
            return 1;
        }
        
        string final_resp(final_response, bytes_received);
        if (final_resp == "OK") {
            // Authentication successful, start chatting
            chat_with_server(client_socket, username);
        } else {
            cout << "Unexpected final response from server: " << final_resp << endl;
        }
    } else if (response == "FAIL") {
        cout << "Authentication failed. Incorrect password." << endl;
    } else {
        cout << "Unexpected response from server: " << response << endl;
    }

    // 8. Close the socket.
    close(client_socket);
    return 0;
}