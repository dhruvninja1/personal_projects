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
    
        std::string perms = getPermissions(fileStat);
        std::cout << perms << "  " << fileStat.st_size << "  " << entry->d_name << std::endl;
    }
    
    closedir(dir);
    return 0;
}

std::string getPermissions(const struct stat &s) {
    std::string perms = "---------";
    if (s.st_mode & S_IRUSR) perms[0] = 'r';
    if (s.st_mode & S_IWUSR) perms[1] = 'w';
    if (s.st_mode & S_IXUSR) perms[2] = 'x';
    if (s.st_mode & S_IRGRP) perms[3] = 'r';
    if (s.st_mode & S_IWGRP) perms[4] = 'w';
    if (s.st_mode & S_IXGRP) perms[5] = 'x';
    if (s.st_mode & S_IROTH) perms[6] = 'r';
    if (s.st_mode & S_IWOTH) perms[7] = 'w';
    if (s.st_mode & S_IXOTH) perms[8] = 'x';
    return perms;
}
