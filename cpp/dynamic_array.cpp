#include <iostream>
#include <unistd.h>
#include <cstddef>
#include <new>
using namespace std;

template <typename T>
class DynamicArray {
    private:
        T* data;
        size_t size;
        size_t capacity;

        void resize(){
            size_t new_capacity = capacity*2;
            T* new_Data = new T[new_capacity];
            for (size_t i = 0; i < size; ++i){
                new_Data[i] = data[i];
            }
            if (data != nullptr){
                delete[] data;
            }
            data = new_Data;
            capacity = new_capacity;
        }
    public:
        DynamicArray() {
            capacity = 10;
            size = 0;
            data = new T[capacity];
        }
        ~DynamicArray(){
            delete[] data;
        }

        T at(size_t index){
            if (index >= size) {
                throw out_of_range("Index out of range");
            }

            return data[index];
        }
        void push_back(T arg){
            if (size == capacity){
                resize();
            }
            data[size] = arg;
            size++;
            return;
        }
        size_t getSize(){
            return size;
        }
        size_t getCapacity(){
            return capacity;
        }
};


int main(){
    DynamicArray<int> test;
    for(int i = 0; i < 15; i++){
        test.push_back(i);
        cout << "hi " << test.getCapacity() << endl;
    }
}