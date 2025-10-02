[BITS 32]
global start
extern kmain

start:
    ; We should already be in protected mode with proper segments
    ; but let's make sure
    mov ax, 0x10       ; data segment selector
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000   ; safe stack (same as bootloader)

    ; Clear BSS section (if any)
    ; Not needed for our simple kernel but good practice
    
    call kmain         ; jump to C kernel

halt_loop:
    cli                ; disable interrupts
    hlt
    jmp halt_loop