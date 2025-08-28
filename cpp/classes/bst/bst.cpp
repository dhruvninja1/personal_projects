
#include <BST.h> // Include your header file to get the class definition.

// Implementation of the BST class methods.

// Constructor
BST::BST() : root(nullptr) {}

// Destructor
BST::~BST() {
    deleteTreeRecursive(root);
}

// Public insert method
void BST::insert(int value) {
    root = insertRecursive(root, value);
}

// Public search method
bool BST::search(int value) {
    return searchRecursive(root, value);
}

// Public inorder traversal method
void BST::inorderTraversal() {
    std::cout << "In-order traversal (sorted): ";
    inOrderTraversalRecursive(root);
    std::cout << std::endl;
}

// Private recursive helper methods.

Node* BST::insertRecursive(Node* current, int value) {
    if (current == nullptr) {
        return new Node(value);
    }
    if (value < current->data) {
        current->left = insertRecursive(current->left, value);
    } else if (value > current->data) {
        current->right = insertRecursive(current->right, value);
    }
    return current;
}

bool BST::searchRecursive(Node* current, int value) {
    if (current == nullptr) {
        return false;
    }
    if (current->data == value) {
        return true;
    }
    if (value < current->data) {
        return searchRecursive(current->left, value);
    } else {
        return searchRecursive(current->right, value);
    }
}

void BST::deleteTreeRecursive(Node* current) {
    if (current == nullptr) {
        return;
    }
    deleteTreeRecursive(current->left);
    deleteTreeRecursive(current->right);
    delete current;
}

void BST::inOrderTraversalRecursive(Node* current) {
    if (current == nullptr) {
        return;
    }
    inOrderTraversalRecursive(current->left);
    std::cout << current->data << " ";
    inOrderTraversalRecursive(current->right);
}
