#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;

int main(){
    int a = 0;
    string line;
    getline(cin, line);
    istringstream iss(line);
    int number;
    while (iss >> number){
        if (number % 2 == 1){
            a = a + number;
        }
    }
    cout << a;
}
