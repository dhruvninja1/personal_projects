#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string scheme;
    string str;
    cin >> scheme;
    cin >> str;
    bool flag=true;

    int len = str.length();
    for (int i=0; i<len; i++){
        if (str[i] == scheme[i] || scheme[i] == '*'){
            
        }
        else{
            flag=false;
            break;
        }
    }
    if (flag){
        cout << "True";

    }
    else{
        cout << "False";
    }

}