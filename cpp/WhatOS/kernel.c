typedef unsigned char bool;
#define true 1
#define false 0
#define NULL ((void*)0)
int row = 0;
int col = 0;
typedef unsigned char  uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int   uint32_t;
typedef unsigned long  uint64_t;
typedef unsigned int size_t;

static char *vga = (char*)0xB8000;
#define INPUT_MAX 128
char input[INPUT_MAX];
int input_len = 0;

// --- Keyboard scancode table ---
static const char keymap[128] = {
    0,  27, '1','2','3','4','5','6','7','8','9','0','-','=', '\b',
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n', 0,
    'a','s','d','f','g','h','j','k','l',';','\'','`',   0,'\\',
    'z','x','c','v','b','n','m',',','.','/',   0, '*',  0,' ',
    // rest is empty
};




// memory function declerations
void *memset(void *dest, int val, size_t len);
void *memcpy(void *dest, const void *src, size_t len);
void *memmove(void *dest, const void *src, size_t len);
int memcmp(const void *a, const void *b, size_t len);
int strcmp(const char *a, const char *b);


// string function declerations
size_t strlen(const char *s);
int strcmp(const char *a, const char *b);
int strncmp(const char *a, const char *b, size_t n);
char *strcpy(char *dest, const char *src);
char *strncpy(char *dest, const char *src, size_t n);
char *strcat(char *dest, const char *src);
char *strchr(const char *s, int c);

// other
int atoi(const char *s);
int powi(int base, int exp);

// kernel function declerations
void handle_command(const char *cmd);
void putchar(char c);
void print(const char *msg);
void clear_screen(void);
void handle_enter();



// memory functions
void *memset(void *dest, int val, size_t len){
    unsigned char *ptr = (unsigned char*)dest;
    for (size_t i = 0; i < len; i++) {
        ptr[i] = (unsigned char)val;
    }
    return dest;
}

void *memcpy(void *dest, const void *src, size_t len) {
    unsigned char *ptr = (unsigned char*)dest;
    const unsigned char *ptr2 = (const unsigned char*)src;
    for (size_t i = 0; i < len; i++) {
        ptr[i] = ptr2[i];
    }
    return dest;
}

void *memmove(void *dest, const void *src, size_t len) {
    unsigned char *d = (unsigned char*)dest;
    const unsigned char *s = (const unsigned char*)src;

    if (d < s) {
        for (size_t i = 0; i < len; i++) {
            d[i] = s[i];
        }
    } else if (d > s) {
        for (size_t i = len; i != 0; i--) {
            d[i-1] = s[i-1];
        }
    }
    return dest;
}

int memcmp(const void *a, const void *b, size_t len) {
    const unsigned char *p1 = (const unsigned char*)a;
    const unsigned char *p2 = (const unsigned char*)b;

    for (size_t i = 0; i < len; i++) {
        if (p1[i] != p2[i]) {
            return (int)p1[i] - (int)p2[i];
        }
    }
    return 0; 
}

// string functions

size_t strlen(const char *s) {
    size_t size = 0;
    while (s[size] != '\0') {
        size++;
    }
    return size;
}

int strcmp(const char *a, const char *b) {
    while (*a && (*a == *b)) {
        a++;
        b++;
    }
    return *(const unsigned char*)a - *(const unsigned char*)b;
}

int strncmp(const char *a, const char *b, size_t n) {
    for (size_t i = 0; i < n; i++) {
        unsigned char ca = (unsigned char)a[i];
        unsigned char cb = (unsigned char)b[i];

        if (ca != cb) return ca - cb; 
        if (ca == '\0') return 0;
    }
    return 0; 
}

char *strcat(char *dest, const char *src) {
    size_t destlen = strlen(dest);
    size_t i = 0;

    // Append src to dest
    while (src[i] != '\0') {
        dest[destlen + i] = src[i];
        i++;
    }

    dest[destlen + i] = '\0';  // null-terminate
    return dest;
}

char *strchr(const char *s, int c) {
    unsigned char uc = (unsigned char)c;
    while (*s) {
        if ((unsigned char)*s == uc) return (char *)s;
        s++;
    }
    if (uc == 0) return (char *)s; // include null terminator
    return NULL;
}

// other
int atoi(const char *s) {
    int result = 0;
    int sign = 1;
    if (*s == '-') {
        sign = -1;
        s++;
    } else if (*s == '+') {
        s++;
    }

    while (*s) {
        if (*s < '0' || *s > '9') break; 
        result = result * 10 + (*s - '0');
        s++;
    }

    return result * sign;
}

int powi(int base, int exp) {
    int result = 1;
    while (exp > 0) {
        result *= base;
        exp--;
    }
    return result;
}







// kernel functions
static inline uint8_t inb(uint16_t port) {
    uint8_t ret;
    __asm__ volatile ("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}



void putchar(char c) {
    if (c == '\n') {
        row++;
        col = 0;
        return;
    }
    if (c == '\b' && input_len > 0) { // handle backspace
        input_len--;
        col--;
        vga[(row*80 + col)*2] = ' ';
        vga[(row*80 + col)*2+1] = 0x0F;
        return;
    }
    vga[(row*80 + col)*2] = c;
    vga[(row*80 + col)*2 + 1] = 0x0F;
    col++;
}

void handle_enter() {
    input[input_len] = '\0';   // null terminate
    handle_command(input);
    input_len = 0;
    row++;
    col = 0;
}

void print(const char *msg) {
    for (int i = 0; msg[i]; i++) {
        putchar(msg[i]);
    }
}

void clear_screen(void) {
    char *vga = (char*)0xB8000;
    int i;
    for (i = 0; i < 80 * 25; i++) {
        vga[i*2] = ' ';      // space character
        vga[i*2 + 1] = 0x07; // attribute: white on black
    }

    // Reset cursor position
    row = 0;
    col = 0;
}

void handle_command(const char *cmd) {
    print("\n");
    if (!strcmp(cmd, "clear")) {
        clear_screen();
    } else if (!strcmp(cmd, "hello")) {
        print("Hello back!\n");
    } else {
        print("Unknown command\n");
    }
}


void kmain(void) {
    // Use a simple approach first
    char *vga = (char*)0xB8000;
    const char *nl = "\n";
    const char *msg = "Hello Kernel!";
    int i;


    clear_screen();
    
    // Clear first line
    print(msg);
    print(nl);
    print(msg);
    while (1) {
        if (inb(0x64) & 1) {         
            uint8_t sc = inb(0x60);   
            if (!(sc & 0x80)) {     
                if (sc == 0x1C) { // Enter key scancode
                    handle_enter();
                } else {
                    char c = keymap[sc];
                    if (c) {
                        input[input_len++] = c;
                        putchar(c);
                    }
                }
            }
        }
    }

    // Halt loop
    while(1) { 
        __asm__ volatile ("cli; hlt"); 
    }
}
