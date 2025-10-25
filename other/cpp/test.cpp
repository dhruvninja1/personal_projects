#include <iostream>
#include <vector>
using namespace std;


int main() {
    int n, p; cin >> n >> p;
    cout << (n*n + n - p*p + p + 4)/2;
}