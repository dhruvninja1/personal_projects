#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(){
    while (1){
        char cwd[1024];
        printf("%s", getcwd(cwd, sizeof(cwd)));
        printf(" # ");
        char command[100];
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0;
        
        if (strcmp(command, "exit") == 0){
            printf("Goodbye!\n");
            exit(0);
        }
        
        // Handle cd command specially
        if (strncmp(command, "cd ", 3) == 0) {
            char *path = command + 3;
            if (chdir(path) != 0) {
                perror("cd");
            }
        } else {
            system(command);
        }
    }
    return 0;
}