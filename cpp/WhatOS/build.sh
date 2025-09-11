#!/bin/bash

# === File names ===
BOOT_ASM="boot.asm"
KERNEL_C="kernel.c"
KEYBOARD_C="keyboard.c"
KERNEL_ENTRY="kernel_entry.asm"
INTERRUPTS_ASM="interrupts.asm"
LINKER_SCRIPT="linker.ld"
BOOT_BIN="boot.bin"
KERNEL_BIN="kernel.bin"
KERNEL_ENTRY_OBJ="kernel_entry.o"
INTERRUPTS_OBJ="interrupts.o"
KERNEL_C_OBJ="kernel.o"
KEYBOARD_C_OBJ="keyboard.o"
OS_IMG="os.img"

# Clean previous builds
rm -f $BOOT_BIN $KERNEL_BIN $KERNEL_ENTRY_OBJ $INTERRUPTS_OBJ $KERNEL_C_OBJ $KEYBOARD_C_OBJ $OS_IMG

# === Compiler detection ===
if command -v i386-elf-gcc &> /dev/null; then
    COMPILER="i386-elf-gcc"
    OBJCOPY="i386-elf-objcopy"
    echo "Using cross-compiler: $COMPILER"
elif command -v i386-linux-gnu-gcc &> /dev/null; then
    COMPILER="i386-linux-gnu-gcc"
    OBJCOPY="i386-linux-gnu-objcopy"
    echo "Using cross-compiler: $COMPILER"
elif command -v gcc &> /dev/null; then
    COMPILER="gcc"
    OBJCOPY="objcopy"
    echo "Using system GCC with -m32 (multilib required): $COMPILER"
else
    echo "Error: No suitable compiler found (need i386-elf-gcc or gcc)."
    exit 1
fi

# === Assemble kernel entry point ===
echo "Assembling kernel entry point..."
nasm -f elf32 $KERNEL_ENTRY -o $KERNEL_ENTRY_OBJ
if [ $? -ne 0 ]; then
  echo "Kernel entry assembly failed!"
  exit 1
fi

# === Assemble interrupt handlers ===
echo "Assembling interrupt handlers..."
nasm -f elf32 $INTERRUPTS_ASM -o $INTERRUPTS_OBJ
if [ $? -ne 0 ]; then
  echo "Interrupt handlers assembly failed!"
  exit 1
fi

# === Compile the C kernel ===
echo "Compiling C kernel..."
$COMPILER -m32 -ffreestanding -fno-pie -nostdlib -c $KERNEL_C -o $KERNEL_C_OBJ \
    -Wall -Wextra -fno-stack-protector -fno-builtin
if [ $? -ne 0 ]; then
  echo "Kernel compilation failed!"
  exit 1
fi

# === Compile keyboard handler ===
echo "Compiling keyboard handler..."
$COMPILER -m32 -ffreestanding -fno-pie -nostdlib -c $KEYBOARD_C -o $KEYBOARD_C_OBJ \
    -Wall -Wextra -fno-stack-protector -fno-builtin
if [ $? -ne 0 ]; then
  echo "Keyboard compilation failed!"
  exit 1
fi

# === Link kernel ===
echo "Linking kernel..."
$COMPILER -m32 -ffreestanding -nostdlib -T $LINKER_SCRIPT -o $KERNEL_BIN \
    $KERNEL_ENTRY_OBJ $INTERRUPTS_OBJ $KERNEL_C_OBJ $KEYBOARD_C_OBJ -lgcc
if [ $? -ne 0 ]; then
  echo "Kernel linking failed!"
  exit 1
fi

# Convert to binary format
$OBJCOPY -O binary $KERNEL_BIN $KERNEL_BIN.tmp
mv $KERNEL_BIN.tmp $KERNEL_BIN

# === Assemble the bootloader ===
echo "Assembling bootloader..."
nasm -f bin $BOOT_ASM -o $BOOT_BIN
if [ $? -ne 0 ]; then
  echo "Bootloader assembly failed!"
  exit 1
fi

# === Build the disk image ===
echo "Creating disk image..."
# Create a 1.44MB floppy image filled with zeros
dd if=/dev/zero of=$OS_IMG bs=512 count=2880

# Write bootloader to first sector
dd if=$BOOT_BIN of=$OS_IMG bs=512 count=1 conv=notrunc

# Write kernel starting at second sector
dd if=$KERNEL_BIN of=$OS_IMG bs=512 seek=1 conv=notrunc

echo "Build complete!"
echo "Files created:"
echo "  - $OS_IMG (disk image)"
echo "  - $BOOT_BIN (bootloader)"
echo "  - $KERNEL_BIN (kernel binary)"

# === Run with QEMU ===
echo "Running QEMU..."
qemu-system-x86_64 -fda $OS_IMG -boot a