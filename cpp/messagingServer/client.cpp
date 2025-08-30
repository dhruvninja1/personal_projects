#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <termios.h>

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
const string COLOR_RED = "\033[31m";           // Red for admin notifications
const string COLOR_BOLD_YELLOW = "\033[1;33m"; // Bold yellow for admin status
const string COLOR_DIM = "\033[2m";            // Dim text for history

bool is_admin = false;
string encryption_key; // Will store admin password for encryption
string current_input = ""; // Global variable to store current typing

// XOR encryption/decryption using admin password as key
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

string process_mentions_for_display(const string& message, const string& current_username) {
    string processed = message;
    
    // Process mention markers
    size_t pos = 0;
    while ((pos = processed.find("MENTION_START@", pos)) != string::npos) {
        size_t end_pos = processed.find("MENTION_END", pos);
        if (end_pos != string::npos) {
            string mentioned_user = processed.substr(pos + 14, end_pos - pos - 14); // Skip "MENTION_START@"
            
            // Check if this user is the current user (mentioned)
            string clean_current_username = current_username;
            if (clean_current_username.find("[ADMIN] ") == 0) {
                clean_current_username = clean_current_username.substr(8);
            }
            
            if (mentioned_user == clean_current_username) {
                // This user was mentioned - highlight in yellow
                string highlight = COLOR_YELLOW + "@" + mentioned_user + COLOR_RESET;
                processed.replace(pos, end_pos - pos + 11, highlight); // +11 for "MENTION_END"
                pos += highlight.length();
            } else {
                // Someone else was mentioned - just show normally
                processed.replace(pos, end_pos - pos + 11, "@" + mentioned_user);
                pos += mentioned_user.length() + 1;
            }
        } else {
            break;
        }
    }
    
    return processed;
}

void restore_input_line() {
    if (!current_input.empty()) {
        cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << current_input << flush;
    } else {
        cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << flush;
    }
}

// Function to handle sending and receiving messages after successful authentication.
void chat_with_server(int client_socket, const string& username) {
    char buffer[1024] = {0};

    cout << "Authentication successful! You can now send messages." << endl;
    if (is_admin) {
        cout << COLOR_BOLD_YELLOW << "You are logged in as an ADMIN!" << COLOR_RESET << endl;
        cout << "Admin commands: admin.mute <username>, admin.kick <username>, admin.unmute <username>" << endl;
    }
    cout << "Messages are automatically encrypted for secure communication!" << endl;
    cout << "You can mention users with @username - mentions will be highlighted in yellow!" << endl;
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
            else if (current_input == "cmd.skull"){
                current_input = "💀";
            }
            
            string message_to_send;
            
            // Check if it's an admin command (send as-is, don't format with username)
            if (is_admin && current_input.find("admin.") == 0) {
                message_to_send = current_input;
            } else {
                // Format regular message with username
                message_to_send = username + " - " + current_input;
            }
            
            // Encrypt the message before sending
            string encrypted_message = encrypt_message(message_to_send, encryption_key);
            send(client_socket, encrypted_message.c_str(), encrypted_message.length(), 0);
            
            current_input = ""; // Clear the input after sending
            cout << COLOR_MAGENTA << "You >> " << COLOR_RESET << flush; // Show prompt for next message
        }

        if (FD_ISSET(client_socket, &read_fds)) {
            memset(buffer, 0, sizeof(buffer));
            ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
            if (bytes_received > 0) {
                string encrypted_message(buffer, bytes_received);
                
                // Decrypt the received message
                string received_message = decrypt_message(encrypted_message, encryption_key);
                
                // Clear the current prompt line
                cout << "\r\033[K"; // Move to beginning of line and clear it
                
                // Handle special admin messages
                if (received_message.find("ADMIN_MUTE:") == 0) {
                    string notification = received_message.substr(11);
                    cout << COLOR_RED << notification << COLOR_RESET << endl;
                }
                else if (received_message.find("ADMIN_KICK:") == 0) {
                    string notification = received_message.substr(11);
                    cout << COLOR_RED << notification << COLOR_RESET << endl;
                    cout << "Connection will be closed..." << endl;
                    break; // Exit the chat loop
                }
                else if (received_message.find("ADMIN_UNMUTE:") == 0) {
                    string notification = received_message.substr(13);
                    cout << COLOR_LIGHT_GREEN << notification << COLOR_RESET << endl;
                }
                else if (received_message.find("ADMIN_ERROR:") == 0) {
                    string error = received_message.substr(12);
                    cout << COLOR_RED << "Admin Error: " << error << COLOR_RESET << endl;
                }
                else if (received_message.find("MUTED:") == 0) {
                    string mute_msg = received_message.substr(6);
                    cout << COLOR_RED << mute_msg << COLOR_RESET << endl;
                }
                else if (received_message.find("HISTORY:") == 0) {
                    // Display history messages in dimmed color
                    string history_msg = received_message.substr(8);
                    history_msg = process_mentions_for_display(history_msg, username);
                    
                    // Find the dash separator to split username and message
                    size_t dash_pos = history_msg.find(" - ");
                    if (dash_pos != string::npos) {
                        string sender_name = history_msg.substr(0, dash_pos);
                        string actual_message = history_msg.substr(dash_pos + 3);
                        
                        // Display history with dim formatting
                        if (sender_name.find("[ADMIN]") != string::npos) {
                            cout << COLOR_DIM << COLOR_BOLD_YELLOW << sender_name << COLOR_RESET << COLOR_DIM << " - " << actual_message << COLOR_RESET << endl;
                        } else {
                            cout << COLOR_DIM << COLOR_CYAN << sender_name << COLOR_RESET << COLOR_DIM << " - " << actual_message << COLOR_RESET << endl;
                        }
                    } else {
                        cout << COLOR_DIM << history_msg << COLOR_RESET << endl;
                    }
                }
                // Check if it's a join/leave message
                else if (received_message.find(" has joined the chat!") != string::npos) {
                    // Display join messages in light green
                    cout << COLOR_LIGHT_GREEN << received_message << COLOR_RESET << endl;
                } 
                else if (received_message.find(" has left the chat!") != string::npos) {
                    // Display leave messages in light red
                    cout << COLOR_LIGHT_RED << received_message << COLOR_RESET << endl;
                }
                else if (received_message.find(" has been muted by ") != string::npos ||
                         received_message.find(" has been kicked by ") != string::npos ||
                         received_message.find(" has been unmuted by ") != string::npos) {
                    // Display admin action messages in red
                    cout << COLOR_RED << received_message << COLOR_RESET << endl;
                }
                else {
                    // Process mentions for display
                    string display_message = process_mentions_for_display(received_message, username);
                    
                    // Find the dash separator to split username and message
                    size_t dash_pos = display_message.find(" - ");
                    if (dash_pos != string::npos) {
                        string sender_name = display_message.substr(0, dash_pos);
                        string actual_message = display_message.substr(dash_pos + 3);
                        
                        // Highlight admin messages differently
                        if (sender_name.find("[ADMIN]") != string::npos) {
                            cout << COLOR_BOLD_YELLOW << sender_name << COLOR_RESET << " - " << actual_message << endl;
                        } else {
                            cout << COLOR_CYAN << sender_name << COLOR_RESET << " - " << actual_message << endl;
                        }
                    } else {
                        // Fallback if message doesn't have expected format
                        cout << display_message << endl;
                    }
                }
                
                // Restore the prompt with any previously typed text
                restore_input_line();
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
    char auth_response[256] = {0}; // Increased buffer size to accommodate key
    ssize_t bytes_received = recv(client_socket, auth_response, sizeof(auth_response) - 1, 0);
    if (bytes_received <= 0) {
        cerr << "Error receiving authentication response." << endl;
        close(client_socket);
        return 1;
    }

    string response(auth_response, bytes_received);
    if (response == "PASSWORD_OK") {
        cout << "Password accepted. Sending username..." << endl;
    } else if (response == "ADMIN_OK") {
        cout << COLOR_BOLD_YELLOW << "Admin password accepted! You have admin privileges." << COLOR_RESET << endl;
        cout << "Sending username..." << endl;
        is_admin = true;
    } else if (response.substr(0, 3) == "KEY") {
        // Server sent encryption key (admin password)
        encryption_key = response.substr(4); // Remove "KEY:" prefix
        cout << "Password accepted. Encryption key received. Sending username..." << endl;
    } else if (response.substr(0, 9) == "ADMIN_KEY") {
        // Admin authentication with key
        encryption_key = response.substr(10); // Remove "ADMIN_KEY:" prefix
        cout << COLOR_BOLD_YELLOW << "Admin password accepted! You have admin privileges." << COLOR_RESET << endl;
        cout << "Encryption key received. Sending username..." << endl;
        is_admin = true;
    } else if (response == "FAIL") {
        cout << "Authentication failed. Incorrect password." << endl;
        close(client_socket);
        return 1;
    } else {
        cout << "Unexpected response from server: " << response << endl;
        close(client_socket);
        return 1;
    }

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

    // 10. Close the socket.
    close(client_socket);
    return 0;
}