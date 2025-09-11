#include <iostream>
#include <string>
using namespace std;

int main(){
    string inputstr;
    string str;
    getline(cin, inputstr);
    int size = inputstr.length();
    for (int i=0; i<size; i++){
        if (inputstr[i] != ' '){
            str += inputstr[i];
        }
    }

    bool flag= true;
    size = str.length();

    transform(str.begin(), str.end(), str.begin(), ::tolower);

    for (int i=0; i<size; i++){
        if (str[i] != str[size-1-i]){
            flag=false;
            break;
        }
    }
    if (flag){
        cout << "yes";
    }
    else{
        cout << "no";
    }
}