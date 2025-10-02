#pragma once

#include <iostream>
#include <cstddef>

template <typename T>
class DLL {
    private:
        // Struct definition is a good fit for the header
        struct Node{
            size_t data;
            Node* next;
            Node* prev;
            Node(T Value) : data(Value), next(nullptr), prev(nullptr) {}
        };

        Node* head;
        Node* tail;

    public:
        // Function declarations (prototypes)
        DLL() : head(nullptr), tail(nullptr) {}
        ~DLL();
        void push_front(T value);
        void push_back(T value);
        void pop_front();
        void pop_back();
        void display_forward();
        void display_backwards();
};
