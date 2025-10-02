#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void compress_file(const string input_filename, const string output_filename){
    ifstream input_file(input_filename, ios::binary);
    ofstream output_file(output_filename, ios::binary);
    if (!input_file.is_open() || !output_file.is_open()){
        cerr << "Could not open file." << endl;
        return;
    }
    char current_byte;

    char next_byte;
    int count = 1;

    if (input_file.get(current_byte)){
        while (input_file.get(next_byte)){
            if (current_byte == next_byte && count < 255){
                count ++;
            }
            else{
                output_file.put(static_cast<unsigned char>(count));
                output_file.put(current_byte);
                current_byte = next_byte;
                count = 1;
            }
        }
        output_file.put(static_cast<char>(count));
        output_file.put(current_byte);
    }
}


void decompress_file(const string input_filename, const string output_filename){
    ifstream input_file(input_filename, ios::binary);
    ofstream output_file(output_filename, ios::binary);
    if (!input_file.is_open() || !output_file.is_open()){
        cerr << "Could not open file." << endl;
        return;
    }

    char count_byte;
    char data_byte;
    while (input_file.get(count_byte) && input_file.get(data_byte)){
        int count = static_cast<unsigned char>(count_byte);
        for(int i=0; i<count; ++i){
            output_file.put(data_byte);
        }
    }
}


int main(int argc, char* argv[]){
    if (argc != 4){
        cerr << "Usage: " << argv[0] << " <option> <input_file> <output_file>" << endl;
        cerr << "Options: -c (compress) or -d (decompress)" << endl;
        return 1;
    }
    string option = argv[1];
    string input_filename = argv[2];
    string output_filename = argv[3];

    if (option == "-c"){
        compress_file(input_filename, output_filename);
        cout << "File compressed successfully!" << endl;
    }
    else if (option == "-d"){
        decompress_file(input_filename, output_filename);
        cout << "File decompressed successfully!" << endl;
    }
    else{
        cerr << "Invalid option. Use -c or -d." << endl;
        return 1;
    }
    return 0;
}