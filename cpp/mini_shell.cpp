#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(){
    std::string line;
    while (true){
        std::cout << "mysh> ";
        char cwd[1024]; // buffer for current directory
        if (getcwd(cwd, sizeof(cwd)) != nullptr) {
            std::cout << cwd << " > ";
        } else {
            perror("getcwd");
            std::cout << "mysh> ";
        }

        std::getline(std::cin, line);
        if (line.empty()) continue;
        if (line == "exit") break;
        std::istringstream iss(line);
        std::vector<std::string> args;
        std::string arg;
        while (iss >> arg){
            args.push_back(arg);
        }

        if (args[0] == "cd") {
            const char* dir = (args.size() > 1) ? args[1].c_str(): getenv("HOME");
            if (chdir(dir) == -1) {
                perror("cd");
            }
            continue;
        }

        std::vector<char*> c_args;
        for (auto &s : args) {
            c_args.push_back(&s[0]);
        }
        c_args.push_back(nullptr);

        std::string outFile;
        bool redirect = false;

        // Check for ">" in args
        for (size_t i = 0; i < args.size(); ++i) {
            if (args[i] == ">") {
                if (i + 1 < args.size()) {
                    outFile = args[i + 1]; // output file
                    args.resize(i);        // remove ">" and filename from args
                    redirect = true;
                } else {
                    std::cerr << "Syntax error: no file after '>'\n";
                }
                break;
            }
        }
        pid_t pid = fork();
        if (pid == 0) {
            if (redirect) {
                int fd = open(outFile.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
                if (fd < 0) {
                    perror("open");
                    exit(1);
                }
                dup2(fd, STDOUT_FILENO); // redirect stdout to file
                close(fd);
            }
            
            if (execvp(c_args[0], c_args.data()) == -1) {
                perror("execvp");
            }
            exit(1);
        }
        else if (pid > 0) {
            int status;
            waitpid(pid, &status, 0);
        } 
        else {
            perror("fork");
        }
        
    
    }
    std::cout << "Goodbye!\n";
    return 0;
}