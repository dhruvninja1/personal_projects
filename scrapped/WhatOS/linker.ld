ENTRY(start)
SECTIONS
{
    . = 0x1000;       /* must match bootloader load address */
    .text : { *(.text) }
    .data : { *(.data) }
    .bss  : { *(.bss) *(COMMON) }
}
