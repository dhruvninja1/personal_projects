#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int a;
    int b;
    vector<int> c;
    while (cin >> a >> b){
        c.push_back(a+b);
    }

    for (int i = 0; i<c.size(); i++){
        cout << c[i] << endl;
    }

}