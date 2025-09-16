#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int count = 0;
    int a;
    int b;
    cin >> a >> b;
    int digits = 0;
    string t;

    for (int i=1;  i<=a; i++){
        digits = 1;
        t = to_string(i);
        for (int j=0; j<t.length(); j++){
            digits = digits * (t[j]-'0');
        }
        if (abs(i - digits) <= b){count++;}
    }
    cout << count;
}