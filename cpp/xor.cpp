#include <iostream>
#include <fstream>
#include <string>
#include <random>
using namespace std;

string generate_salt(size_t length){
    string salt;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(0, 255);
    for (size_t i = 0; i < length; ++i){
        salt += static_cast<char>(distrib(gen));
    }
    return salt;
}

void encrypt(const string input_filename, const string output_filename, const string key, const int salt_length){
    if (key.empty()){
        cerr << "Error: Key empty" << endl;
        return;
    }
    ifstream input_file(input_filename, ios::binary);
    ofstream output_file(output_filename, ios::binary);
    if (!input_file.is_open() || !output_file.is_open()) {
        cerr << "Could not open file." << endl;
        return;
    }
    string salt = generate_salt(salt_length);
    unsigned char salt_len_byte = static_cast<unsigned char>(salt_length);
    output_file.put(salt_len_byte);
    output_file.write(salt.c_str(), salt_length);
    string combined_key = salt + key;
    char byte;
    size_t key_index = 0;
    char key_byte;
    while (input_file.get(byte)){
        key_byte = combined_key[key_index % combined_key.length()];
        char processed_byte = byte ^ key_byte;
        output_file.put(processed_byte);
        key_index++;
    }
}

void decrypt(const string input_filename, const string output_filename, const string key){
    if (key.empty()){
        cerr << "Error: Key empty" << endl;
        return;
    }
    ifstream input_file(input_filename, ios::binary);
    ofstream output_file(output_filename, ios::binary);
    if (!input_file.is_open() || !output_file.is_open()) {
        cerr << "Could not open file." << endl;
        return;
    }
    unsigned char salt_length_byte;
    input_file.get(reinterpret_cast<char&>(salt_length_byte));
    size_t salt_length = salt_length_byte;
    string salt(salt_length, '\0');
    input_file.read(&salt[0], salt_length);
    string combined_key = salt + key;
    char byte;
    size_t key_index = 0;
    char key_byte;
    while (input_file.get(byte)){
        key_byte = combined_key[key_index % combined_key.length()];
        char processed_byte = byte ^ key_byte;
        output_file.put(processed_byte);
        key_index++;
    }
}


int main(int argc, char* argv[]){
    
    string operation = argv[1];
    if (operation == "-e"){
        if (argc != 6) {
            cerr << "Usage: " << argv[0] << " <operator> <input_file> <output_file> <key> <salt length>" << endl;
            cerr << "Operators: -e, -d" << endl;
            return 1;
        }
    }
    else if (operation == "-d"){
        if (argc != 5) {
            cerr << "Usage: " << argv[0] << " <operator> <input_file> <output_file> <key>" << endl;
            cerr << "Operators: -e, -d" << endl;
            return 1;
        }
    }
    else{
        cerr << "Usage: " << argv[0] << " <operator> <input_file> <output_file> <key> <salt length>" << endl;
        cerr << "Operators: -e, -d" << endl;
    }
    string input_filename = argv[2];
    string output_filename = argv[3];
    string key = argv[4];
    int salt_length;
    if (operation == "-e")
    {
        try{
            salt_length = stoi(argv[5]);
        }
        catch(const invalid_argument& io){
            cerr << "Error: Salt length must be a number." << endl;
            return 1;
        }
        if (salt_length > 255 || salt_length < 0){
            cerr << "Invalid salt_length" << endl;
            return 1;
        }
    }
    if (operation == "-e"){
        encrypt(input_filename, output_filename, key, salt_length);
    }
    else if(operation == "-d"){
        decrypt(input_filename, output_filename, key);
    }
    cout << "Done!" << endl;
    return 0;
}
