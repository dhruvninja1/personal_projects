#include <iostream>
#include <dirent.h>
#include <sys/stat.h>
#include <cstring>

int main(int argc, char *argv[]) {
    const char *path = (argc > 1) ? argv[1] : ".";

    DIR *dir = opendir(path);
    if (!dir) {
        perror("opendir");
        return 1;
    }

    struct dirent *entry;
    struct stat fileStat;

    while ((entry = readdir(dir)) != nullptr) {
        std::string fullPath = std::string(path) + "/" + entry->d_name;

        if (stat(fullPath.c_str(), &fileStat) == -1) {
            perror("stat");
            continue;
        }

       std::cout << fileStat.st_size << "  " << entry->d_name << std::endl;
    }

    closedir(dir);
    return 0;
}
