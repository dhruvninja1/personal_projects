#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int a; cin >> a;
    int den = 0;
    float sum = 0;
    for (int i = 1; i<=a; i++){
        den += i*2;
        sum += 1.0/den;
    }
    cout << den;

}
