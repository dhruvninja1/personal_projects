// BST.h
#ifndef BST_H
#define BST_H

#include <iostream>
struct Node {
    int data;
    Node* left;
    Node* right;

    Node(int value) : data(value), left(nullptr), right(nullptr) {}
};

class BST {
private:
    Node* root;

    Node* insertRecursive(Node* current, int value);
    bool searchRecursive(Node* current, int value);
    void deleteTreeRecursive(Node* current);
    void inOrderTraversalRecursive(Node* current);

public:
    BST();
    ~BST();
    void insert(int value);
    bool search(int value);
    void inorderTraversal();
};

#endif
