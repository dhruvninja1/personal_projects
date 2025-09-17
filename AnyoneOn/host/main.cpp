#ifdef __linux__
#include <crow.h>
#include <crow/json.h>
#elif __APPLE__
#include "crow_all.h"
#endif

#include <fstream>
#include <mutex>
#include <vector>
#include <string>

using namespace std;

struct Status{
    string user;
    string status;
};

vector<Status> statuses;
mutex mtx;

void read_file(string file, vector<crow::json::wvalue>& arr);
string strip_quotes(const string& s);

int main(int argc, char* argv[]){
    int PORT;
    if (argc != 2){
        cout << "Enter port only";
        return 1;
    }
    else{
        PORT = stoi(argv[1]);
    }
    string file = "data/" + to_string(PORT) + ".json";
    crow::json::wvalue obj;
    auto arr = vector<crow::json::wvalue>();
    read_file(file, arr);
    crow::SimpleApp app;
    CROW_ROUTE(app, "/status").methods(crow::HTTPMethod::OPTIONS)
    ([](){
        crow::response res;
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.code = 204;
        return res;
    });

    CROW_ROUTE(app, "/statuses").methods(crow::HTTPMethod::OPTIONS)
    ([](){
        crow::response res;
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "GET, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.code = 204;
        return res;
    });

    CROW_ROUTE(app, "/status").methods(crow::HTTPMethod::POST)
    ([&arr, &file](const crow::request& req){
        lock_guard<mutex> lock(mtx);
        ofstream out(file);
        auto r = crow::json::load(req.body);
        bool found = false;

        for (size_t i = 0; i < arr.size(); ++i) {
            auto& tempObj = arr[i];
            if (tempObj.count("name") && strip_quotes(tempObj["name"].dump()) == static_cast<string>(r["name"])) {
                found = true;
                tempObj["status"] = r["status"];
                break;
            }
        }
        
        if (!found){
            crow::json::wvalue tempObj2;
            tempObj2["name"] = r["name"].s();
            tempObj2["status"] = r["status"].s();
            arr.push_back(move(tempObj2));
        }
        crow::json::wvalue result = arr;
        out << result.dump();
        
        crow::response res;
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.set_header("Content-Type", "application/json");
        res.code = 200;
        res.body = "{\"success\": true}";
    
    return res;
    });

    CROW_ROUTE(app, "/statuses")
    ([&arr, &file]() {
        crow::response res;
        res.set_header("Access-Control-Allow-Origin", "*");
        lock_guard<mutex> lock(mtx);
        read_file(file, arr);
        crow::json::wvalue result = arr;
        return crow::response(result.dump());
    });



    app.port(PORT).multithreaded().run();
}


string strip_quotes(const string& s){
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"')
        return s.substr(1, s.size() - 2);
    return s;
}

void read_file(string file, vector<crow::json::wvalue>& arr){
    ifstream in(file);
    if (in.is_open()) {
        string content((istreambuf_iterator<char>(in)),
                             istreambuf_iterator<char>());
        if (!content.empty()) {
            auto parsed = crow::json::load(content);
            if (parsed && parsed.t() == crow::json::type::List) {
                arr.clear();
                for (size_t i = 0; i < parsed.size(); ++i) {
                    arr.push_back(parsed[i]);
                }
            }
        }
    }
}
