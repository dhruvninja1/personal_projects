#include <iostream>
using namespace std;


unsigned long long fib_iterative(int a){
    unsigned long long n1 = 0;
    unsigned long long n2 = 1;
    unsigned long long temp = 0;
    for (int i=1; i<a; i++){
        temp = n1+n2;
        n1 = n2;
        n2 = temp % 1000000007;
    }
    return n2;
}

int main(){
    int a; cin >> a;
    cout << fib_iterative(a);
}