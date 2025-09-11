#include "interrupts.h"

// IDT with 256 entries
static idt_entry_t idt[256];
static idt_ptr_t idt_ptr;

// Video memory for displaying characters
static char* video_memory = (char*)0xb8000;
static int cursor_x = 0;
static int cursor_y = 0;

// Basic scan code to ASCII table (US keyboard layout)
static unsigned char scancode_to_ascii[] = {
    0,    0,   '1',  '2',  '3',  '4',  '5',  '6',  // 0x00-0x07
    '7',  '8',  '9',  '0',  '-',  '=',  0,    0,    // 0x08-0x0F
    'q',  'w',  'e',  'r',  't',  'y',  'u',  'i',  // 0x10-0x17
    'o',  'p',  '[',  ']',  '\n', 0,    'a',  's',  // 0x18-0x1F
    'd',  'f',  'g',  'h',  'j',  'k',  'l',  ';',  // 0x20-0x27
    '\'', '`',  0,    '\\', 'z',  'x',  'c',  'v',  // 0x28-0x2F
    'b',  'n',  'm',  ',',  '.',  '/',  0,    0,    // 0x30-0x37
    0,    ' ',  0,    0,    0,    0,    0,    0,    // 0x38-0x3F
};

// Shifted characters
static unsigned char scancode_to_ascii_shift[] = {
    0,    0,   '!',  '@',  '#',  '$',  '%',  '^',  // 0x00-0x07
    '&',  '*',  '(',  ')',  '_',  '+',  0,    0,    // 0x08-0x0F
    'Q',  'W',  'E',  'R',  'T',  'Y',  'U',  'I',  // 0x10-0x17
    'O',  'P',  '{',  '}',  '\n', 0,    'A',  'S',  // 0x18-0x1F
    'D',  'F',  'G',  'H',  'J',  'K',  'L',  ':',  // 0x20-0x27
    '"',  '~',  0,    '|',  'Z',  'X',  'C',  'V',  // 0x28-0x2F
    'B',  'N',  'M',  '<',  '>',  '?',  0,    0,    // 0x30-0x37
    0,    ' ',  0,    0,    0,    0,    0,    0,    // 0x38-0x3F
};

// Keyboard state
static int shift_pressed = 0;

// Put a character on screen at current cursor position
void putchar(char c) {
    if (c == '\n') {
        cursor_x = 0;
        cursor_y++;
    } else {
        int offset = (cursor_y * 80 + cursor_x) * 2;
        video_memory[offset] = c;
        video_memory[offset + 1] = 0x0F;  // White on black
        cursor_x++;
        if (cursor_x >= 80) {
            cursor_x = 0;
            cursor_y++;
        }
    }
    
    // Simple scrolling - just wrap to top (you can improve this)
    if (cursor_y >= 25) {
        cursor_y = 0;
    }
}

// Set up an IDT entry
void set_idt_entry(int index, unsigned int handler_address) {
    idt[index].offset_low = handler_address & 0xFFFF;
    idt[index].selector = 0x08;  // Code segment from GDT
    idt[index].zero = 0;
    idt[index].type_attr = 0x8E; // Present, ring 0, 32-bit interrupt gate
    idt[index].offset_high = (handler_address >> 16) & 0xFFFF;
}

// Initialize IDT
void setup_idt(void) {
    // Clear IDT
    for (int i = 0; i < 256; i++) {
        set_idt_entry(i, 0);
    }
    
    // Set keyboard interrupt (IRQ1 = interrupt 33)
    set_idt_entry(33, (unsigned int)keyboard_interrupt_handler);
    
    // Set up IDT pointer
    idt_ptr.limit = sizeof(idt) - 1;
    idt_ptr.base = (unsigned int)idt;
    
    // Load IDT
    load_idt(&idt_ptr);
}

// Initialize PIC (Programmable Interrupt Controller)
void setup_pic(void) {
    // Remap PIC interrupts (avoid conflict with CPU exceptions)
    outb(0x20, 0x11); // Initialize master PIC
    outb(0x21, 0x20); // Master PIC vector offset (32)
    outb(0x21, 0x04); // Tell master PIC about slave
    outb(0x21, 0x01); // 8086 mode
    
    outb(0xA0, 0x11); // Initialize slave PIC  
    outb(0xA1, 0x28); // Slave PIC vector offset (40)
    outb(0xA1, 0x02); // Tell slave PIC about master
    outb(0xA1, 0x01); // 8086 mode
    
    // Enable keyboard interrupt (IRQ1)
    outb(0x21, 0xFD); // Enable IRQ1, disable others
    outb(0xA1, 0xFF); // Disable all slave PIC interrupts
}

// Main keyboard setup function
void setup_keyboard(void) {
    setup_idt();
    setup_pic();
    enable_interrupts();
    
    // Print setup message
    const char* msg = "\nKeyboard initialized! Start typing:\n";
    for (int i = 0; msg[i] != '\0'; i++) {
        putchar(msg[i]);
    }
}

// C keyboard interrupt handler (called from assembly)
void keyboard_handler_c(void) {
    unsigned char scancode = inb(0x60); // Read scan code
    putchar('*'); // DEBUG
    
    // Check if key press (not release)
    if (scancode < 0x80) {
        // Handle special keys
        if (scancode == 0x2A || scancode == 0x36) { // Left/right shift
            shift_pressed = 1;
            return;
        }
        
        // Convert scan code to ASCII
        char ascii = 0;
        if (scancode < sizeof(scancode_to_ascii)) {
            if (shift_pressed) {
                ascii = scancode_to_ascii_shift[scancode];
            } else {
                ascii = scancode_to_ascii[scancode];
            }
        }
        
        // Display character if valid
        if (ascii != 0) {
            putchar(ascii);
        }
    } else {
        // Key release
        scancode &= 0x7F; // Remove release bit
        if (scancode == 0x2A || scancode == 0x36) { // Shift released
            shift_pressed = 0;
        }
    }
}