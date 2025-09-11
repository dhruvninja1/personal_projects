void main() {
    char* video_memory = (char*)0xb8000;

    const char* message = "Hello, C kernel!";
    for (int i = 0; message[i] != '\0'; i++) {
        *video_memory = message[i];
        video_memory += 2; 
    }

    while (1) {}
}
