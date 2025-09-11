#ifndef INTERRUPTS_H
#define INTERRUPTS_H

// Assembly function declarations
extern unsigned char inb(unsigned short port);
extern void outb(unsigned short port, unsigned char value);
extern void load_idt(void* idt_ptr);
extern void enable_interrupts(void);
extern void keyboard_interrupt_handler(void);

// IDT entry structure (8 bytes each)
typedef struct {
    unsigned short offset_low;    // Lower 16 bits of handler address
    unsigned short selector;      // Code segment selector
    unsigned char zero;           // Always 0
    unsigned char type_attr;      // Type and attributes
    unsigned short offset_high;   // Upper 16 bits of handler address
} __attribute__((packed)) idt_entry_t;

// IDT pointer structure (for lidt instruction)
typedef struct {
    unsigned short limit;         // Size of IDT - 1
    unsigned int base;            // Address of IDT
} __attribute__((packed)) idt_ptr_t;

// Function declarations
void setup_idt(void);
void setup_keyboard(void);
void keyboard_handler_c(void);
void putchar(char c);

#endif