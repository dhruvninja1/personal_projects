// DynamicArray.h - The Header File
// For template classes, the full implementation must be in the header.
// This is because the compiler needs access to all the code to generate
// the specialized class for each data type (e.g., DynamicArray<int>).

#pragma once

#include <cstddef>      // For size_t
#include <stdexcept>    // For std::out_of_range
#include <new>          // For std::bad_alloc
#include <utility>      // For std::move
#include <iostream>     // For std::cerr in the resize() function

template <typename T>
class DynamicArray {
private:
    T* data;
    size_t arraySize;
    size_t arrayCapacity;

    // Private helper function to double the capacity
    void resize() {
        size_t new_capacity = (arrayCapacity == 0) ? 1 : arrayCapacity * 2;
        
        try {
            // Allocate new memory for the bigger array
            T* new_Data = new T[new_capacity];
            
            // Move elements from the old array to the new one
            for (size_t i = 0; i < arraySize; ++i) {
                // Using std::move is more efficient for complex types
                new_Data[i] = std::move(data[i]);
            }
            
            // Deallocate the old memory
            if (data != nullptr) {
                delete[] data;
            }
            
            // Update the pointers and capacity
            data = new_Data;
            arrayCapacity = new_capacity;
        } catch (const std::bad_alloc& e) {
            std::cerr << "Memory allocation failed during resize: " << e.what() << std::endl;
            throw; // Re-throw the exception
        }
    }
    
public:
    // Default constructor
    DynamicArray() : data(nullptr), arraySize(0), arrayCapacity(0) {}

    // Destructor to clean up dynamically allocated memory
    ~DynamicArray() {
        delete[] data;
        data = nullptr;
    }
    
    // Copy constructor (Rule of Three/Five)
    DynamicArray(const DynamicArray& other) : 
        arraySize(other.arraySize), 
        arrayCapacity(other.arrayCapacity) {
        data = new T[arrayCapacity];
        for (size_t i = 0; i < arraySize; ++i) {
            data[i] = other.data[i];
        }
    }

    // Copy assignment operator (Rule of Three/Five)
    DynamicArray& operator=(const DynamicArray& other) {
        if (this != &other) {
            delete[] data;
            arraySize = other.arraySize;
            arrayCapacity = other.arrayCapacity;
            data = new T[arrayCapacity];
            for (size_t i = 0; i < arraySize; ++i) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }

    // Move constructor (Rule of Five)
    DynamicArray(DynamicArray&& other) noexcept :
        data(other.data),
        arraySize(other.arraySize),
        arrayCapacity(other.arrayCapacity) {
        other.data = nullptr;
        other.arraySize = 0;
        other.arrayCapacity = 0;
    }

    // Move assignment operator (Rule of Five)
    DynamicArray& operator=(DynamicArray&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            arraySize = other.arraySize;
            arrayCapacity = other.arrayCapacity;
            other.data = nullptr;
            other.arraySize = 0;
            other.arrayCapacity = 0;
        }
        return *this;
    }

    // Access an element at a given index with bounds checking
    T& at(size_t index) {
        if (index >= arraySize) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    // Constant version of at()
    const T& at(size_t index) const {
        if (index >= arraySize) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    // Add an element to the end of the array
    void push_back(const T& arg) {
        if (arraySize == arrayCapacity) {
            resize();
        }
        data[arraySize++] = arg;
    }

    // Get the current number of elements
    size_t getSize() const {
        return arraySize;
    }

    // Get the current allocated capacity
    size_t getCapacity() const {
        return arrayCapacity;
    }
};
