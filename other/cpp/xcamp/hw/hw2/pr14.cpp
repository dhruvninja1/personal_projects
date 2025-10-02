#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int num;
    string str;
    cin >> str;
    int len = str.length();
    for (int i=0; i < len-1; i++){
        if (str[i] == 'X' && str[i+1] == 'C'){num++;}
    }
    cout << num;
}