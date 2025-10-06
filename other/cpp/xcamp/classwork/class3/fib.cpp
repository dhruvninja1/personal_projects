#include <iostream>
#include "bigint.h"
using namespace std;


bigint fib_recursive(int a){
    cout << 'a';
    if (a==1){return 1;}
    if (a==0){return 0;}
    return fib_recursive(a-1) + fib_recursive(a-2);
}


bigint fib_iterative(int a){
    bigint n1 = 1;
    bigint n2 = 2;
    bigint temp = 0;
    for (int i=1; i<a; i++){
        temp = n1+n2;
        n1 = n2;
        n2 = temp;
    }
    return n2;
}

int main(){
    int a; cin >> a;
    cout << fib_iterative(a);
}