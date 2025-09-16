#include <crow.h>
#include <crow/json.h>
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

int main(){
    crow::SimpleApp app;
    CROW_ROUTE(app, "/status")
    ([](const crow::request& req){
        return crow::response();
    });

    CROW_ROUTE(app, "/statuses")
    ([](const crow::request& req){
        return crow::response();
    });



    app.port(18080).multithreaded().run();
}