#include <iostream>

using namespace std;

void func(int a){
    if (a==1){cout << 1 << " "; return;}
    else{
      func(floor(a/2));
      cout << a << " ";
      func(a-floor(a/2));
    }
}



int main(){
  int a; cin >> a;
  func(a);
}