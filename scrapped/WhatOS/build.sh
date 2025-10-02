#!/bin/bash
set -e

# Assemble kernel entry
nasm -f elf32 kernel_entry.asm -o kernel_entry.o

# Compile C kernel
i386-elf-gcc -m32 -ffreestanding -O2 -c kernel.c -o kernel.o

# Link kernel
i386-elf-ld -T linker.ld -o kernel.elf kernel_entry.o kernel.o

# Convert to binary
i386-elf-objcopy -O binary kernel.elf kernel.bin

# Create floppy image
dd if=/dev/zero of=floppy.img bs=512 count=2880

# Write bootloader
nasm -f bin boot.asm -o boot.bin
dd if=boot.bin of=floppy.img bs=512 count=1 conv=notrunc

# Write kernel after bootloader
dd if=kernel.bin of=floppy.img bs=512 seek=1 conv=notrunc

# Boot in QEMU
qemu-system-i386 -fda floppy.img
