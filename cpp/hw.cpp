#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main(){
    int a;
    cin >> a;
    if (a % 5 == 0 || (a % 3 == 0 && a <= 20)){
        cout << "YES";
    }
    else{
        cout << "NO";
    }
}

