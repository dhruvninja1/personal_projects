#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main(){
    int a;
    cin >> a;
    vector<unsigned long long> nums;
    unsigned long long temp;
    for (int i=0; i<a; i++){
        cin >> temp;
        nums.push_back(temp);
    }

    unsigned long long min = 1234567898765;
    unsigned long long max = 0;
    for (int o = 0; o<a; o++){
        if (nums[o] > max){
            max = nums[o];
        }
        if (nums[o] < min){
            min = nums[o];
        }

    }

    cout << max << endl << min;
}




