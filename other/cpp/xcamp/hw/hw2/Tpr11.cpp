#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int num;
    cin >> num;
    int output = 0;
    while (output != 1){
        if (num % 2 == 1){
            output = num * 3 + 1;
            cout << num << "*3+1=" << output  << endl;
        }
        else if (num % 2 == 0){
            output = num/2;
            cout << num << "/2=" << output << endl;
        }
        num = output;
    }
    cout << "End" << endl;

}