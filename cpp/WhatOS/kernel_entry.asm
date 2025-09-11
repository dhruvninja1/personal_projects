[bits 32]
[extern kernel_main]

global _start
_start:
    ; Set up segments for protected mode
    mov ax, 0x10    ; Data segment selector
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    
    ; Set up stack (important!)
    mov esp, 0x90000
    mov ebp, esp
    
    ; Clear direction flag
    cld
    
    ; Call the C kernel
    call kernel_main
    
    ; Should never reach here, but just in case
halt_loop:
    hlt
    jmp halt_loop

; Mark stack as non-executable (reduces warnings)
section .note.GNU-stack noalloc noexec nowrite progbits