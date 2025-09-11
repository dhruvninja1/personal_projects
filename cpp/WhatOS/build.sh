#!/bin/bash

# Define output file names
BOOT_ASM="boot.asm"
KERNEL_C="kernel.c"
BOOT_BIN="boot.bin"
KERNEL_BIN="kernel.bin"
OS_IMG="os.img"

# Define the cross-compiler name
CROSS_COMPILER="i386-elf-gcc"

# Check for the required cross-compiler
if ! command -v $CROSS_COMPILER &> /dev/null
then
    # If not found, try common Homebrew locations on macOS
    if [[ -d "/opt/homebrew/bin" ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
    fi
    if [[ -d "/usr/local/bin" ]]; then
        export PATH="/usr/local/bin:$PATH"
    fi

    if ! command -v $CROSS_COMPILER &> /dev/null
    then
        echo "Error: $CROSS_COMPILER could not be found."
        echo "Please ensure the cross-compiler is installed and in your PATH."
        exit 1
    fi
fi

# Compile the C kernel to a 32-bit flat binary using the cross-compiler
# -m32: Compile for 32-bit architecture
# -ffreestanding: Do not link the standard C library
# -fno-pie: Disable Position Independent Executables
# -nostdlib: Do not link standard libraries
# -Ttext=0x10000: Set the entry point of the binary to 0x10000
# -Wl,--build-id=none: A fix for some versions of GCC to not embed build IDs
echo "Compiling C kernel..."
$CROSS_COMPILER -m32 -ffreestanding -fno-pie -nostdlib -o $KERNEL_BIN -Ttext=0x10000 -Wl,--build-id=none $KERNEL_C

# Check if GCC compilation was successful
if [ $? -ne 0 ]; then
  echo "GCC compilation failed!"
  exit 1
fi

# Assemble the bootloader
echo "Assembling bootloader..."
nasm -f bin $BOOT_ASM -o $BOOT_BIN

# Check if NASM assembly was successful
if [ $? -ne 0 ]; then
  echo "NASM assembly failed!"
  exit 1
fi

# Concatenate the bootloader and kernel into a single disk image
echo "Creating disk image..."
dd if=$BOOT_BIN of=$OS_IMG bs=512 count=1 conv=notrunc
dd if=$KERNEL_BIN of=$OS_IMG bs=512 seek=1 conv=notrunc

# Pad the disk image to a minimum of 1.44MB for a virtual floppy
# This is required by QEMU for floppy emulation.
echo "Padding disk image to 1.44MB..."
dd if=/dev/zero of=$OS_IMG bs=512 seek=2880 count=0 conv=notrunc

# Run the disk image with QEMU
echo "Running QEMU..."
qemu-system-x86_64 -fda $OS_IMG -boot a
