bits 16
org 0x7C00

start:
    cli
    xor ax, ax
    mov ss, ax
    mov sp, 0x7C00
    mov [BOOT_DRIVE], dl

    ; Print "Booting..."
    mov si, boot_msg
print_loop:
    lodsb
    test al, al
    jz load_kernel
    mov ah, 0x0E
    int 0x10
    jmp print_loop

load_kernel:
    ; Load kernel
    mov ah, 0x02        ; BIOS read sectors
    mov al, 8           ; number of sectors 
    mov ch, 0
    mov cl, 2           ; first sector after boot
    mov dh, 0
    mov dl, [BOOT_DRIVE]
    mov bx, 0x1000      ; load address
    int 0x13
    jc disk_error

    ; Setup GDT and enter protected mode
    cli
    lgdt [gdt_descriptor]
    
    ; Enable A20 line
    in al, 0x92
    or al, 2
    out 0x92, al

    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; Far jump to protected mode
    jmp 0x08:init_pm

bits 32
init_pm:
    ; Setup segments
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000    ; Set up stack

    ; Jump to kernel
    jmp 0x1000

bits 16
disk_error:
    mov si, error_msg
error_print:
    lodsb
    test al, al
    jz halt
    mov ah, 0x0E
    int 0x10
    jmp error_print

halt:
    hlt
    jmp halt

boot_msg: db 'Booting...', 13, 10, 0
error_msg: db 'Disk Error!', 13, 10, 0
BOOT_DRIVE: db 0

; Simple GDT
gdt_start:
    dq 0x0000000000000000       ; null descriptor
    dq 0x00CF9A000000FFFF       ; code segment (0x08)
    dq 0x00CF92000000FFFF       ; data segment (0x10)
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

times 510-($-$$) db 0
dw 0xAA55