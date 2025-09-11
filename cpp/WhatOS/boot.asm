; === BOOTLOADER ===
;
; This bootloader is loaded by the BIOS into memory at 0x7C00.
; Its job is to set up a new stack, enter 32-bit protected mode,
; and jump to the C kernel.

[org 0x7c00]      ; Tell the assembler that the code will be loaded at 0x7c00
[bits 16]         ; We start in 16-bit real mode

; === MAIN ENTRY POINT ===
; This is where the BIOS will jump to after loading the boot sector.
main:
    ; Set up the stack
    mov ax, 0x07c0
    mov ss, ax
    mov sp, 0x7c00

    ; Print "Booting..." message to the screen
    mov ah, 0x0e      ; TTY mode
    mov al, 'B'
    int 0x10
    mov al, 'o'
    int 0x10
    mov al, 'o'
    int 0x10
    mov al, 't'
    int 0x10
    mov al, 'i'
    int 0x10
    mov al, 'n'
    int 0x10
    mov al, 'g'
    int 0x10
    mov al, '.'
    int 0x10
    mov al, '.'
    int 0x10
    mov al, '.'
    int 0x10

    ; --- Protected Mode Switch ---
    ; This code sets up the GDT and enters protected mode, which is required
    ; to run a C kernel.
    cli                      ; Clear interrupts
    lgdt [gdt_descriptor]    ; Load GDT descriptor
    mov eax, cr0             ; Get a copy of the control register
    or eax, 0x1              ; Set the protected mode bit (PE)
    mov cr0, eax             ; Set the control register
    jmp 0x08:protected_mode  ; Far jump to our new segment and start protected mode

; === GLOBAL DESCRIPTOR TABLE (GDT) ===
; This table defines the memory segments for protected mode.
gdt_start:
    ; Null descriptor
    gdt_null: db 0,0,0,0,0,0,0,0
    ; Code segment descriptor
    gdt_code: dw 0xffff          ; Limit (0-15)
              dw 0x0000          ; Base (0-15)
              db 0x00            ; Base (16-23)
              db 10011010b       ; Access byte
              db 11001111b       ; Flags (limit 16-19)
              db 0x00            ; Base (24-31)
    ; Data segment descriptor
    gdt_data: dw 0xffff
              dw 0x0000
              db 0x00
              db 10010010b
              db 11001111b
              db 0x00
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; === 32-BIT PROTECTED MODE CODE ===
; This section runs after the far jump and prepares the environment for the C kernel.
[bits 32]
protected_mode:
    ; Set up all segment registers with the new data segment
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000         ; Set up a stack for our C kernel

    ; Final jump to the C kernel's entry point
    jmp dword 0x10000        ; Jump to the C kernel at address 0x10000

; === BOOT SECTOR PADDING ===
; This section pads the file to be exactly 512 bytes long and adds the boot signature.
times 510 - ($ - $$) db 0
dw 0xaa55
