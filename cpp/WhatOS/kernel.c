#include "interrupts.h"
void simple_putchar(char c) {
    static int pos = 80*2*2; // Start on line 2
    char* video_memory = (char*)0xb8000;
    video_memory[pos] = c;
    video_memory[pos + 1] = 0x0F;
    pos += 2;
}

// Add proper function attributes to prevent issues
void __attribute__((noreturn)) kernel_main(void);

void kernel_main() {
    // Clear screen first
    char* video_memory = (char*)0xb8000;
    
    // Clear the entire screen (80x25 = 2000 characters, 2 bytes each)
    for (int i = 0; i < 80 * 25 * 2; i += 2) {
        video_memory[i] = ' ';      // Space character
        video_memory[i + 1] = 0x07; // White on black attribute
    }
    
    // Reset to beginning of screen
    video_memory = (char*)0xb8000;
    
    const char* message = "Hello, C kernel! Boot successful!";
    for (int i = 0; message[i] != '\0'; i++) {
        video_memory[i * 2] = message[i];     // Character
        video_memory[i * 2 + 1] = 0x0F;      // White on black attribute
    }

    // Setup keyboard
    putchar('D');
    setup_keyboard();


    // Infinite loop to prevent returning
    while (1) {
        // Halt instruction to save CPU cycles
        __asm__ volatile ("hlt");
    }
}