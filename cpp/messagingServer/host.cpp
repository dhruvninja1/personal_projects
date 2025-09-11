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
#include <set>
#include <sstream>
#include <fstream>
#include <deque>

using namespace std;

struct ChatRoom {
    string name;
    set<int> clients;
    deque<string> message_history;
    string history_filename;
    
    // Default constructor
    ChatRoom() : name("") {
        // Empty default constructor
    }
    
    ChatRoom(const string& room_name, const string& logs_dir = "") : name(room_name) {
        if (logs_dir.empty()) {
            history_filename = room_name + "_history.txt";
        } else {
            history_filename = logs_dir + "/" + room_name + "_history.txt";
        }
        load_history();
    }
    
    void load_history();
    void save_message(const string& message);
    void send_history_to_client(int client_fd);
};

// Function declarations
void broadcast_message_to_room(const string& message, const string& room_name, int sender_fd = -1);
bool set_non_blocking(int fd);
void remove_client(int fd);
void handle_admin_command(const string& message, int admin_fd);
void handle_room_command(const string& message, int client_fd);
string process_mentions(const string& message);
void log_server_event(const string& event);
void save_rooms_list();
void load_rooms_list();
bool is_image_message(const string& message);
void handle_image_message(const string& message, int sender_fd);
string extract_image_filename(const string& message);

// Global variables
vector<int> client_sockets;
string SERVER_PASSWORD;
string ADMIN_PASSWORD;
string ROOMS_LOGS_DIR;
map<string, ChatRoom> chat_rooms;
map<int, bool> authenticated_clients;
map<int, string> client_usernames;
map<int, int> client_auth_stage;
map<int, bool> admin_clients;
map<int, bool> muted_clients;
map<int, string> client_current_room;

// ChatRoom method implementations
void ChatRoom::load_history() {
    if (name.empty()) return;
    
    ifstream file(history_filename);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            message_history.push_back(line);
        }
        file.close();
        
        // Keep only last 100 messages in memory
        if (message_history.size() > 100) {
            message_history.erase(message_history.begin(), 
                                message_history.end() - 100);
        }
    }
}

void ChatRoom::save_message(const string& message) {
    // Save normal chat messages and image messages
    if (message.find("ROOM_") == 0 || 
        message.find("USERS_LIST:") == 0 || 
        message.find("ADMIN_") == 0 || 
        message.find("MUTED:") == 0) {
        return;
    }

    message_history.push_back(message);
    if (message_history.size() > 100) {
        message_history.pop_front();
    }

    // For image messages, we might want to save them differently or limit storage
    bool is_image = is_image_message(message);
    
    ofstream file(history_filename, ios::app);
    if (file.is_open()) {
        if (is_image) {
            // Save image metadata instead of full data to save space
            string filename = extract_image_filename(message);
            string sender = message.substr(0, message.find(" - "));
            file << sender << " - [IMAGE: " << filename << "]" << endl;
        } else {
            file << message << endl;
        }
        file.close();
    }
}

void ChatRoom::send_history_to_client(int client_fd) {
    int start_index = max(0, (int)message_history.size() - 50);
    
    for (int i = start_index; i < (int)message_history.size(); i++) {
        string history_msg = "HISTORY:" + message_history[i];
        send(client_fd, history_msg.c_str(), history_msg.length(), 0);
        usleep(10000); // Small delay to ensure messages arrive in order
    }
}

bool set_non_blocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return false;
    flags |= O_NONBLOCK;
    return fcntl(fd, F_SETFL, flags) != -1;
}

bool is_image_message(const string& message) {
    return message.find("IMAGE_START|") != string::npos && 
           message.find("|IMAGE_END") != string::npos;
}

string extract_image_filename(const string& message) {
    size_t start = message.find("IMAGE_START|");
    if (start == string::npos) return "unknown.jpg";
    
    start = message.find("|", start + 12); // Skip messageId
    if (start == string::npos) return "unknown.jpg";
    
    start++; // Move past the |
    size_t end = message.find("|", start);
    if (end == string::npos) return "unknown.jpg";
    
    return message.substr(start, end - start);
}

void handle_image_message(const string& message, int sender_fd) {
    if (!authenticated_clients.count(sender_fd) || !authenticated_clients[sender_fd]) {
        return;
    }
    
    if (!client_current_room.count(sender_fd) || client_current_room[sender_fd].empty()) {
        string error_msg = "ROOM_ERROR:You must join a room first to send images.";
        send(sender_fd, error_msg.c_str(), error_msg.length(), 0);
        return;
    }
    
    string current_room = client_current_room[sender_fd];
    string filename = extract_image_filename(message);
    
    // Log image transmission
    log_server_event("Image '" + filename + "' sent to room '" + current_room + 
                    "' by '" + client_usernames[sender_fd] + "'");
    
    // Find the room and save message
    auto room_it = chat_rooms.find(current_room);
    if (room_it != chat_rooms.end()) {
        room_it->second.save_message(message);
        
        // Broadcast to room (excluding sender)
        broadcast_message_to_room(message, current_room, sender_fd);
    }
}

string process_mentions(const string& message) {
    string processed = message;
    
    size_t pos = 0;
    while ((pos = processed.find("@", pos)) != string::npos) {
        size_t end_pos = pos + 1;
        
        while (end_pos < processed.length() && 
               (isalnum(processed[end_pos]) || processed[end_pos] == '_' || processed[end_pos] == '-')) {
            end_pos++;
        }
        
        if (end_pos > pos + 1) {
            string mentioned_user = processed.substr(pos + 1, end_pos - pos - 1);
            
            bool user_exists = false;
            for (auto& pair : client_usernames) {
                string clean_username = pair.second;
                if (clean_username.find("[ADMIN] ") == 0) {
                    clean_username = clean_username.substr(8);
                }
                if (clean_username == mentioned_user) {
                    user_exists = true;
                    break;
                }
            }
            
            if (user_exists) {
                string mention_marker = "MENTION_START@" + mentioned_user + "MENTION_END";
                processed.replace(pos, end_pos - pos, mention_marker);
                pos += mention_marker.length();
            } else {
                pos = end_pos;
            }
        } else {
            pos = end_pos;
        }
    }
    
    return processed;
}

void log_server_event(const string& event) {
    string logs_dir = "logs";
    if (!ROOMS_LOGS_DIR.empty()) {
        logs_dir = ROOMS_LOGS_DIR.substr(0, ROOMS_LOGS_DIR.find("/rooms"));
    }
    
    string server_log_file = logs_dir + "/server.log";
    ofstream server_log(server_log_file, ios::app);
    if (server_log.is_open()) {
        time_t now = time(0);
        char* dt = ctime(&now);
        dt[strlen(dt)-1] = '\0';
        server_log << "[" << dt << "] " << event << endl;
        server_log.close();
    }
}

void save_rooms_list() {
    if (ROOMS_LOGS_DIR.empty()) return;
    
    string rooms_list_file = ROOMS_LOGS_DIR.substr(0, ROOMS_LOGS_DIR.find("/rooms")) + "/rooms_list.txt";
    ofstream file(rooms_list_file);
    if (file.is_open()) {
        for (auto& room_pair : chat_rooms) {
            file << room_pair.first << endl;
        }
        file.close();
        log_server_event("Rooms list saved to " + rooms_list_file);
    }
}

void load_rooms_list() {
    if (ROOMS_LOGS_DIR.empty()) return;
    
    string rooms_list_file = ROOMS_LOGS_DIR.substr(0, ROOMS_LOGS_DIR.find("/rooms")) + "/rooms_list.txt";
    ifstream file(rooms_list_file);
    if (file.is_open()) {
        string room_name;
        while (getline(file, room_name)) {
            if (!room_name.empty() && chat_rooms.find(room_name) == chat_rooms.end()) {
                chat_rooms[room_name] = ChatRoom(room_name, ROOMS_LOGS_DIR);
                log_server_event("Loaded persistent room: " + room_name);
            }
        }
        file.close();
        log_server_event("Rooms list loaded from " + rooms_list_file);
    }
}

void broadcast_message_to_room(const string& message, const string& room_name, int sender_fd) {
    auto room_it = chat_rooms.find(room_name);
    if (room_it == chat_rooms.end()) return;

    string processed_message;
    
    // Don't process mentions in image messages to avoid corrupting base64 data
    if (is_image_message(message)) {
        processed_message = message;
    } else {
        processed_message = process_mentions(message);
    }

    ChatRoom& room = room_it->second;
    for (int client_fd : room.clients) {
        if (client_fd != sender_fd) {
            ssize_t bytes_sent = send(client_fd, processed_message.c_str(), processed_message.length(), 0);
            if (bytes_sent == -1) {
                if (errno != EWOULDBLOCK && errno != EAGAIN) {
                    cerr << "Error: Failed to send message to client " << client_fd << ". Closing socket." << endl;
                    remove_client(client_fd);
                }
            }
        }
    }
}

void remove_client(int fd) {
    if (authenticated_clients.count(fd) && authenticated_clients[fd]) {
        if (client_usernames.count(fd) && client_current_room.count(fd) && !client_current_room[fd].empty()) {
            string current_room = client_current_room[fd];
            string leave_message = client_usernames[fd] + " has left the chat!";
            broadcast_message_to_room(leave_message, current_room, fd);
            
            log_server_event("User '" + client_usernames[fd] + "' disconnected from room '" + current_room + "'");
            
            if (chat_rooms.find(current_room) != chat_rooms.end()) {
                chat_rooms[current_room].clients.erase(fd);
            }
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
    client_current_room.erase(fd);
    close(fd);
}

int find_client_by_username(const string& username) {
    for (auto& pair : client_usernames) {
        string clean_username = pair.second;
        if (clean_username.find("[ADMIN] ") == 0) {
            clean_username = clean_username.substr(8);
        }
        if (clean_username == username) {
            return pair.first;
        }
    }
    return -1;
}

void handle_room_command(const string& message, int client_fd) {
    if (message.find("/join ") == 0) {
        string room_name = message.substr(6);
        
        room_name.erase(0, room_name.find_first_not_of(" \t\r\n"));
        room_name.erase(room_name.find_last_not_of(" \t\r\n") + 1);
        
        cout << "Attempting to join room: '" << room_name << "'" << endl;
        log_server_event("Join request for room: '" + room_name + "' by '" + client_usernames[client_fd] + "'");
        
        if (chat_rooms.find(room_name) == chat_rooms.end()) {
            string error_msg = "ROOM_ERROR:Room '" + room_name + "' does not exist. Use /rooms to see available rooms.";
            send(client_fd, error_msg.c_str(), error_msg.length(), 0);
            return;
        }
        
        if (client_current_room.count(client_fd) && !client_current_room[client_fd].empty()) {
            string old_room = client_current_room[client_fd];
            if (chat_rooms.find(old_room) != chat_rooms.end()) {
                chat_rooms[old_room].clients.erase(client_fd);
                
                string leave_msg = client_usernames[client_fd] + " has left " + old_room;
                broadcast_message_to_room(leave_msg, old_room, client_fd);
                log_server_event("User '" + client_usernames[client_fd] + "' left room '" + old_room + "'");
            }
        }
        
        auto room_it = chat_rooms.find(room_name);
        if (room_it != chat_rooms.end()) {
            room_it->second.clients.insert(client_fd);
            client_current_room[client_fd] = room_name;

            string join_info = "ROOM_JOINED:" + room_name;
            send(client_fd, join_info.c_str(), join_info.length(), 0);

            usleep(50000); // 50ms delay

            room_it->second.send_history_to_client(client_fd);

            string join_msg = client_usernames[client_fd] + " has joined " + room_name;
            broadcast_message_to_room(join_msg, room_name, client_fd);
            
            log_server_event("User '" + client_usernames[client_fd] + "' joined room '" + room_name + "'");
        }
    }
    else if (message == "/rooms") {
        string rooms_list = "ROOMS_LIST:Available rooms: ";
        for (auto& room_pair : chat_rooms) {
            rooms_list += room_pair.first + " (" + to_string(room_pair.second.clients.size()) + " users), ";
        }
        if (rooms_list.back() == ' ') rooms_list.pop_back();
        if (rooms_list.back() == ',') rooms_list.pop_back();
        
        send(client_fd, rooms_list.c_str(), rooms_list.length(), 0);
    }
    else if (message == "/who") {
        if (!client_current_room.count(client_fd) || client_current_room[client_fd].empty()) {
            string error_msg = "ROOM_ERROR:You must join a room first to see who's in it.";
            send(client_fd, error_msg.c_str(), error_msg.length(), 0);
            return;
        }
        
        string current_room = client_current_room[client_fd];
        if (chat_rooms.find(current_room) != chat_rooms.end()) {
            string users_list = "USERS_LIST:Users in " + current_room + ": ";
            for (int user_fd : chat_rooms[current_room].clients) {
                if (client_usernames.count(user_fd)) {
                    users_list += client_usernames[user_fd] + ", ";
                }
            }
            if (users_list.back() == ' ') users_list.pop_back();
            if (users_list.back() == ',') users_list.pop_back();
            
            send(client_fd, users_list.c_str(), users_list.length(), 0);
        }
    }
}

void handle_admin_command(const string& message, int admin_fd) {
    string admin_username = client_usernames[admin_fd];
    
    if (message.find("admin.makeroom ") == 0) {
        string room_name = message.substr(15);
        
        if (chat_rooms.find(room_name) != chat_rooms.end()) {
            string error_msg = "ADMIN_ERROR:Room '" + room_name + "' already exists.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
            return;
        }
        
        chat_rooms[room_name] = ChatRoom(room_name, ROOMS_LOGS_DIR);
        
        save_rooms_list();
        
        string success_msg = "ADMIN_SUCCESS:Room '" + room_name + "' created successfully.";
        send(admin_fd, success_msg.c_str(), success_msg.length(), 0);
        
        cout << "Admin " << admin_username << " created room: " << room_name << endl;
        log_server_event("Admin '" + admin_username + "' created room '" + room_name + "'");
        
        string announcement = "ROOM_ANNOUNCEMENT:New room '" + room_name + "' has been created by " + admin_username;
        for (int client_fd : client_sockets) {
            if (client_fd != admin_fd) {
                send(client_fd, announcement.c_str(), announcement.length(), 0);
            }
        }
    }
    else if (message.find("admin.mute ") == 0) {
        string target_username = message.substr(11);
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            muted_clients[target_fd] = true;
            
            string mute_notification = "ADMIN_MUTE:You have been muted by an administrator.";
            send(target_fd, mute_notification.c_str(), mute_notification.length(), 0);
            
            if (client_current_room.count(admin_fd) && !client_current_room[admin_fd].empty()) {
                string current_room = client_current_room[admin_fd];
                string mute_message = target_username + " has been muted by " + admin_username;
                broadcast_message_to_room(mute_message, current_room, admin_fd);
            }
            
            cout << "Admin " << admin_username << " muted user " << target_username << endl;
            log_server_event("Admin '" + admin_username + "' muted user '" + target_username + "'");
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
        }
    }
    else if (message.find("admin.kick ") == 0) {
        string target_username = message.substr(11);
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            string kick_notification = "ADMIN_KICK:You have been kicked by an administrator.";
            send(target_fd, kick_notification.c_str(), kick_notification.length(), 0);
            
            if (client_current_room.count(target_fd) && !client_current_room[target_fd].empty()) {
                string target_room = client_current_room[target_fd];
                string kick_message = target_username + " has been kicked by " + admin_username;
                broadcast_message_to_room(kick_message, target_room, admin_fd);
            }
            
            cout << "Admin " << admin_username << " kicked user " << target_username << endl;
            log_server_event("Admin '" + admin_username + "' kicked user '" + target_username + "'");
            remove_client(target_fd);
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
        }
    }
    else if (message.find("admin.unmute ") == 0) {
        string target_username = message.substr(13);
        int target_fd = find_client_by_username(target_username);
        
        if (target_fd != -1) {
            muted_clients[target_fd] = false;
            
            string unmute_notification = "ADMIN_UNMUTE:You have been unmuted by an administrator.";
            send(target_fd, unmute_notification.c_str(), unmute_notification.length(), 0);
            
            if (client_current_room.count(admin_fd) && !client_current_room[admin_fd].empty()) {
                string current_room = client_current_room[admin_fd];
                string unmute_message = target_username + " has been unmuted by " + admin_username;
                broadcast_message_to_room(unmute_message, current_room, admin_fd);
            }
            
            cout << "Admin " << admin_username << " unmuted user " << target_username << endl;
            log_server_event("Admin '" + admin_username + "' unmuted user '" + target_username + "'");
        } else {
            string error_msg = "ADMIN_ERROR:User '" + target_username + "' not found.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
        }
    }
    else if (message.find("admin.removeroom ") == 0) {
        string room_name = message.substr(17);
        
        if (chat_rooms.find(room_name) == chat_rooms.end()) {
            string error_msg = "ADMIN_ERROR:Room '" + room_name + "' does not exist.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
            return;
        }
        
        if (room_name == "general") {
            string error_msg = "ADMIN_ERROR:Cannot remove the general room.";
            send(admin_fd, error_msg.c_str(), error_msg.length(), 0);
            return;
        }
        
        set<int> users_to_kick;
        for (int client_fd : chat_rooms[room_name].clients) {
            users_to_kick.insert(client_fd);
        }
        
        for (int client_fd : users_to_kick) {
            if (client_current_room.count(client_fd) && client_current_room[client_fd] == room_name) {
                client_current_room[client_fd] = "";
                
                string kick_msg = "ROOM_DELETED:Room '" + room_name + "' has been deleted by an administrator.";
                send(client_fd, kick_msg.c_str(), kick_msg.length(), 0);
            }
        }
        
        chat_rooms.erase(room_name);
        
        string history_file = ROOMS_LOGS_DIR + "/" + room_name + "_history.txt";
        if (remove(history_file.c_str()) == 0) {
            log_server_event("History file deleted: " + history_file);
        } else {
            log_server_event("Warning: Could not delete history file: " + history_file);
        }
        
        save_rooms_list();
        
        string success_msg = "ADMIN_SUCCESS:Room '" + room_name + "' deleted successfully.";
        send(admin_fd, success_msg.c_str(), success_msg.length(), 0);
        
        cout << "Admin " << admin_username << " deleted room: " << room_name << endl;
        log_server_event("Admin '" + admin_username + "' deleted room '" + room_name + "'");
        
        string announcement = "ROOM_ANNOUNCEMENT:Room '" + room_name + "' has been deleted by " + admin_username;
        for (int client_fd : client_sockets) {
            if (client_fd != admin_fd) {
                send(client_fd, announcement.c_str(), announcement.length(), 0);
            }
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
    
    string server_name;
    cout << "Enter server name: ";
    getline(cin, server_name);
    
    string logs_dir = "logs/" + server_name;
    string rooms_dir = logs_dir + "/rooms";
    
    ROOMS_LOGS_DIR = rooms_dir;
    
    system(("mkdir -p " + logs_dir).c_str());
    system(("mkdir -p " + rooms_dir).c_str());
    
    cout << "Logs will be stored in: " << logs_dir << endl;
    
    string server_log_file = logs_dir + "/server.log";
    ofstream server_log(server_log_file, ios::app);
    if (server_log.is_open()) {
        time_t now = time(0);
        char* dt = ctime(&now);
        dt[strlen(dt)-1] = '\0';
        server_log << "[" << dt << "] Server started on port " << PORT << endl;
        server_log << "[" << dt << "] Server name: " << server_name << endl;
        server_log << "[" << dt << "] Image support enabled" << endl;
        server_log.close();
    }
    
    log_server_event("Logging system initialized - logs directory: " + logs_dir);
    log_server_event("Image message handling enabled");

    chat_rooms["general"] = ChatRoom("general", rooms_dir);
    
    load_rooms_list();
    
    cout << "Multi-room chat server with image support starting..." << endl;
    cout << "Default rooms created: general" << endl;
    cout << "Image support: Enabled (max recommended size: 500KB)" << endl;
    
    log_server_event("Default rooms initialized: general");
    log_server_event("Room logs directory: " + rooms_dir);
    
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        cerr << "Error: Failed to create socket." << endl;
        log_server_event("ERROR: Failed to create socket");
        return 1;
    }

    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        cerr << "Error: setsockopt failed." << endl;
        log_server_event("ERROR: setsockopt failed");
        return 1;
    }

    sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if (::bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Error: Failed to bind socket." << endl;
        log_server_event("ERROR: Failed to bind socket");
        close(server_fd);
        return 1;
    }

    if (listen(server_fd, 5) < 0) {
        cerr << "Error: Failed to listen on socket." << endl;
        log_server_event("ERROR: Failed to listen on socket");
        close(server_fd);
        return 1;
    }
    
    set_non_blocking(server_fd);

    int kq_fd = kqueue();
    if (kq_fd == -1) {
        cerr << "Error: kqueue failed." << endl;
        log_server_event("ERROR: kqueue failed");
        return 1;
    }

    struct kevent change_event;
    EV_SET(&change_event, server_fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
    if (kevent(kq_fd, &change_event, 1, NULL, 0, NULL) == -1) {
        log_server_event("ERROR: Failed to add server socket to event loop");
        return 1;
    }

    const int MAX_EVENTS = 128;
    struct kevent event_list[MAX_EVENTS];

    cout << "Server started on port " << PORT << endl;
    cout << "Server name: " << server_name << endl;
    cout << "Regular password: " << SERVER_PASSWORD << endl;
    cout << "Admin password: " << ADMIN_PASSWORD << endl;
    cout << "Plain text communication with image support" << endl;
    
    log_server_event("Server startup complete - listening on port " + to_string(PORT));
    log_server_event("Server configuration - Port: " + to_string(PORT) + ", Server name: " + server_name);

    while (true) {
        int num_events = kevent(kq_fd, NULL, 0, event_list, MAX_EVENTS, NULL);
        if (num_events < 0) {
            cerr << "Error: kevent failed in event loop." << endl;
            log_server_event("ERROR: kevent failed in event loop");
            continue;
        }

        for (int i = 0; i < num_events; ++i) {
            int event_fd = event_list[i].ident;

            if (event_list[i].flags & EV_ERROR || event_list[i].flags & EV_EOF) {
                log_server_event("Client " + to_string(event_fd) + " connection error or EOF");
                remove_client(event_fd);
                continue;
            }

            if (event_fd == server_fd) {
                sockaddr_in client_addr;
                socklen_t client_addr_len = sizeof(client_addr);
                int client_socket = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
                if (client_socket == -1) {
                    log_server_event("ERROR: Failed to accept client connection");
                    continue;
                }
                
                set_non_blocking(client_socket);

                authenticated_clients[client_socket] = false;
                client_auth_stage[client_socket] = 0;
                admin_clients[client_socket] = false;
                muted_clients[client_socket] = false;
                client_current_room[client_socket] = "";
                
                log_server_event("New client connected from " + string(inet_ntoa(client_addr.sin_addr)) + ":" + to_string(ntohs(client_addr.sin_port)));
                log_server_event("Client " + to_string(client_socket) + " added to event loop");

                EV_SET(&change_event, client_socket, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
                if (kevent(kq_fd, &change_event, 1, NULL, 0, NULL) == -1) {
                    log_server_event("ERROR: Failed to add client " + to_string(client_socket) + " to event loop");
                }
            } else {
                char buffer[8192]; // Increased buffer size for image data
                ssize_t bytes_read = recv(event_fd, buffer, sizeof(buffer), 0);
                
                if (bytes_read > 0) {
                    string received_message(buffer, bytes_read);
                    
                    cout << "Received from client " << event_fd << ": message length = " << received_message.length() << endl;
                    
                    // Log first 100 chars for debugging (avoid logging full image data)
                    string debug_msg = received_message.length() > 100 ? 
                                      received_message.substr(0, 100) + "..." : received_message;
                    cout << "Message preview: '" << debug_msg << "'" << endl;

                    if (authenticated_clients.at(event_fd)) {
                        // Check for room commands
                        if (received_message.find("/join ") == 0 || 
                            received_message == "/rooms" || 
                            received_message == "/who") {
                            log_server_event("Room command executed: '" + received_message + "' by '" + client_usernames[event_fd] + "'");
                            handle_room_command(received_message, event_fd);
                        }
                        // Check if this is an admin command
                        else if (admin_clients[event_fd] && (received_message.find("admin.") == 0)) {
                            log_server_event("Admin command executed by '" + client_usernames[event_fd] + "'");
                            handle_admin_command(received_message, event_fd);
                        }
                        // Check if this is an image message
                        else if (is_image_message(received_message)) {
                            cout << "Processing image message from " << client_usernames[event_fd] << endl;
                            handle_image_message(received_message, event_fd);
                        }
                        else {
                            // Check if user is muted
                            if (muted_clients[event_fd]) {
                                string mute_reminder = "MUTED:You are muted and cannot send messages.";
                                send(event_fd, mute_reminder.c_str(), mute_reminder.length(), 0);
                            } else {
                                // Check if user is in a room
                                cout << "User " << client_usernames[event_fd] << " sending regular message. Checking room status..." << endl;
                                
                                if (client_current_room.count(event_fd) && !client_current_room[event_fd].empty()) {
                                    string current_room = client_current_room[event_fd];
                                    
                                    // Find the room and save message
                                    auto room_it = chat_rooms.find(current_room);
                                    if (room_it != chat_rooms.end()) {
                                        room_it->second.save_message(received_message);
                                        
                                        // Log message sent to room
                                        log_server_event("Message sent to room '" + current_room + "' by '" + client_usernames[event_fd] + "'");
                                        
                                        // Broadcast to room
                                        broadcast_message_to_room(received_message, current_room, event_fd);
                                    }
                                } else {
                                    // User not in any room
                                    string error_msg = "ROOM_ERROR:You must join a room first. Use /join <roomname>";
                                    send(event_fd, error_msg.c_str(), error_msg.length(), 0);
                                }
                            }
                        }
                    } else {
                        // Handle authentication stages
                        int stage = client_auth_stage[event_fd];
                        
                        if (stage == 0) {
                            bool is_admin = false;
                            if (received_message == ADMIN_PASSWORD) {
                                is_admin = true;
                                admin_clients[event_fd] = true;
                                send(event_fd, "ADMIN_AUTH_SUCCESS", 18, 0);
                            } else if (received_message == SERVER_PASSWORD) {
                                send(event_fd, "AUTH_SUCCESS", 12, 0);
                            } else {
                                send(event_fd, "FAIL", 4, 0);
                                remove_client(event_fd);
                                continue;
                            }
                            
                            client_auth_stage[event_fd] = 1;
                            cout << "Client " << event_fd << (is_admin ? " (ADMIN)" : "") << " password authenticated. Waiting for username." << endl;
                            log_server_event("Client " + to_string(event_fd) + (is_admin ? " (ADMIN)" : "") + " password authenticated");
                        } else if (stage == 1) {
                            string username = received_message;
                            if (admin_clients[event_fd]) {
                                username = "[ADMIN] " + username;
                            }
                            client_usernames[event_fd] = username;
                            authenticated_clients[event_fd] = true;
                            client_auth_stage[event_fd] = 2;
                            client_sockets.push_back(event_fd);

                            send(event_fd, "OK", 2, 0);
                            
                            log_server_event("User '" + username + "' successfully authenticated");

                            // Auto-join the "general" room
                            string default_room = "general";
                            
                            auto room_it = chat_rooms.find(default_room);
                            if (room_it != chat_rooms.end()) {
                                room_it->second.clients.insert(event_fd);
                                client_current_room[event_fd] = default_room;

                                // Notify the client
                                string join_info = "ROOM_JOINED:" + default_room;
                                send(event_fd, join_info.c_str(), join_info.length(), 0);

                                // Small delay to ensure ROOM_JOINED is processed first
                                usleep(50000); // 50ms delay

                                // Send recent history
                                room_it->second.send_history_to_client(event_fd);

                                // Broadcast join message to other users in general
                                string join_msg = username + " has joined " + default_room;
                                broadcast_message_to_room(join_msg, default_room, event_fd);

                                log_server_event("User '" + username + "' connected and auto-joined room '" + default_room + "'");
                            }
                        }
                    }
                } else if (bytes_read == 0) {
                    log_server_event("Client " + to_string(event_fd) + " disconnected (connection closed)");
                    remove_client(event_fd);
                } else if (errno != EWOULDBLOCK && errno != EAGAIN) {
                    log_server_event("Client " + to_string(event_fd) + " disconnected (error: " + strerror(errno) + ")");
                    remove_client(event_fd);
                }
            }
        }
    }
    return 0;
}