#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main(int argc, char* argv[]){
    int a;
    cin >> a;
    if (a%10 >= 5){
        a += (10-a%10);
    }
    else{
        a -= a%10;
    }
    cout << a;
    
}

