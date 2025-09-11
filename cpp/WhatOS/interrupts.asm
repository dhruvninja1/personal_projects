[bits 32]

; Make functions available to C code
global inb, outb, load_idt, enable_interrupts, keyboard_interrupt_handler

; Declare external C function
extern keyboard_handler_c

section .text

; unsigned char inb(unsigned short port)
; Read a byte from an I/O port
inb:
    push ebp
    mov ebp, esp
    
    mov edx, [ebp + 8]    ; port parameter
    xor eax, eax          ; clear eax
    in al, dx             ; read byte from port into al
    
    pop ebp
    ret

; void outb(unsigned short port, unsigned char value)  
; Write a byte to an I/O port
outb:
    push ebp
    mov ebp, esp
    
    mov edx, [ebp + 8]    ; port parameter
    mov eax, [ebp + 12]   ; value parameter
    out dx, al            ; write byte to port
    
    pop ebp
    ret

; void load_idt(void* idt_ptr)
; Load the Interrupt Descriptor Table
load_idt:
    push ebp
    mov ebp, esp
    
    mov eax, [ebp + 8]    ; idt_ptr parameter
    lidt [eax]            ; load IDT
    
    pop ebp
    ret

; void enable_interrupts(void)
; Enable hardware interrupts
enable_interrupts:
    sti                   ; set interrupt flag
    ret

; Keyboard interrupt handler (called by CPU)
keyboard_interrupt_handler:
    ; Save all registers (interrupt can happen anytime)
    pushad                ; push eax, ecx, edx, ebx, esp, ebp, esi, edi
    
    ; Call our C handler function
    call keyboard_handler_c
    
    ; Send End of Interrupt signal to PIC
    mov al, 0x20          ; EOI command
    out 0x20, al          ; send to master PIC
    
    ; Restore all registers
    popad                 ; pop all registers in reverse order
    
    ; Return from interrupt
    iret                  ; special return for interrupts

; Mark stack as non-executable (reduces linker warnings)
section .note.GNU-stack noalloc noexec nowrite progbits