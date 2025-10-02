#include "DLL.h" // Important: Include the header file
#include <iostream>

using namespace std;

// Class destructor definition
template <typename T>
DLL<T>::~DLL(){
    Node* current = head;
    while (current != nullptr){
        Node* next_node = current->next;
        delete current;
        current = next_node;
    }
}

// Function definitions
template <typename T>
void DLL<T>::push_front(T value){
    Node* new_node = new Node(value);
    if (head == nullptr){
        head = new_node;
        tail = new_node;
    }
    else{
        new_node->next = head;
        head->prev = new_node;
        head = new_node;
    }
}

template <typename T>
void DLL<T>::push_back(T value){
    Node* new_node = new Node(value);
    if (head == nullptr) {
        head = new_node;
        tail = new_node;
    }
    else {
        new_node->prev = tail;
        tail->next = new_node;
        tail = new_node;
    }
}

template <typename T>
void DLL<T>::pop_front(){
    if (head == nullptr){
        return;
    }
    Node* temp = head;
    head = head->next;
    if (head==nullptr){
        tail = nullptr;
    }
    else {
        head->prev = nullptr;
    }
    delete temp;
}

template <typename T>
void DLL<T>::pop_back(){
    if (head == nullptr){
        return;
    }
    Node* temp = tail;
    tail = tail->prev;
    if (tail==nullptr){
        head = nullptr;
    }
    else{
        tail->next = nullptr;
    }
    delete temp;
}

template <typename T>
void DLL<T>::display_forward(){
    Node* current = head;
    if (current == nullptr){
        cout << "Empty" << endl;
        return;
    }
    else{
        while (current != nullptr){
            cout << current->data << " <-> ";
            current = current->next;
        }
    }
    cout << "nullptr" << endl; // Added a better ending
}

template <typename T>
void DLL<T>::display_backwards(){
    Node* current = tail;
    if (current == nullptr){
        cout << "Empty" << endl;
        return;
    }
    else{
        while (current != nullptr){
            cout << current->data << " <-> ";
            current = current->prev;
        }
    }
    cout << "nullptr" << endl; // Added a better ending
}
