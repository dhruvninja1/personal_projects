; === BOOTLOADER ===
; Loads the C kernel from disk into 0x10000 and jumps to it.

[org 0x7c00]
[bits 16]

main:
    ; Save BIOS boot drive (DL contains it at boot)
    mov [BOOT_DRIVE], dl

    ; Setup stack
    mov ax, 0x07c0
    mov ss, ax
    mov sp, 0x7c00

    ; Print "Booting..."
    mov si, boot_msg
.print_char:
    lodsb
    or al, al
    jz .done_print
    mov ah, 0x0e
    int 0x10
    jmp .print_char
.done_print:

    ; === Load kernel (increased from 1 to 4 sectors) ===
    mov ax, 0x1000      ; ES = 0x1000 → segment = 0x10000
    mov es, ax
    mov bx, 0x0000      ; offset
    mov ah, 0x02        ; BIOS: read sectors
    mov al, 4           ; read 4 sectors (2KB - should be enough)
    mov ch, 0           ; cylinder
    mov cl, 2           ; start at sector 2 (bootloader = sector 1)
    mov dh, 0           ; head
    mov dl, [BOOT_DRIVE]
    int 0x13
    jc disk_error       ; if error, show message

    ; Debug: print 'K' if kernel loaded
    mov ah, 0x0e
    mov al, 'K'
    int 0x10

    ; === Enter protected mode ===
    cli
    lgdt [gdt_descriptor]
    mov eax, cr0
    or eax, 0x1
    mov cr0, eax
    jmp 0x08:protected_mode

; === Messages ===
boot_msg db "Booting...", 0
err_msg  db "Disk read error!", 0

; === Disk error handler ===
disk_error:
    mov si, err_msg
.err_loop:
    lodsb
    or al, al
    jz $
    mov ah, 0x0e
    int 0x10
    jmp .err_loop

; === GDT ===
gdt_start:
    dq 0x0000000000000000 ; null
    dq 0x00cf9a000000ffff ; code
    dq 0x00cf92000000ffff ; data
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; === 32-bit protected mode ===
[bits 32]
protected_mode:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000

    ; Jump to C kernel at 0x10000
    jmp 0x10000

; === BIOS drive number ===
BOOT_DRIVE db 0

; === Boot sector padding + signature ===
times 510-($-$$) db 0
dw 0xaa55