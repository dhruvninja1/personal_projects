#include <iostream>
#include <string>
using namespace std;

int main(){
    int a; cin >> a;
    string str;
    string str2 = "";
    getline(cin, str);
    int size = str.length()-1;
    for (int i=size; i>-1; i--){
        str2 += str[i];
    }
    cout << str2;
}
