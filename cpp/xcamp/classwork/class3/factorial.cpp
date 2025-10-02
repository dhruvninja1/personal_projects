#include <iostream>
using namespace std;




uint64_t factorial_loop(int a){
    uint64_t result = 1;
    for (int i = 1; i <= a; i++){
        result *= i;
    }
    return result;
}


uint64_t factorial_recursive(int a){
    uint64_t result;
    if (a == 1){
        result = 1;
        return result;
    }
    result = a * factorial_recursive(a-1);
    return result;
}



int main(){
    int a; cin >> a;
    cout << factorial_loop(a) << endl;
}