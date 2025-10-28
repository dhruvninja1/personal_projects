#include <iostream>
#include <vector>
#include <string>

using namespace std;

int f(int a){
    if (a=0){ return 0;}
    return 2*f(a-1)+1;
}
int main(){
    int a; cin >> a;
    cout << f(a);
}

