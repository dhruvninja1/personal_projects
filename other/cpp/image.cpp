#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <stdexcept>
#include <cstdlib>
#include <sstream> 
using namespace std;


struct Pixel{
    int red;
    int green;
    int blue;

    Pixel() {
        red = 0;
        green = 0;
        blue = 0;
    }
    
    Pixel(int r, int g, int b) {
        red = r;
        green = g;
        blue = b;
    }
};


const Pixel WHITE = Pixel(255, 255, 255);
const Pixel BLACK = Pixel(0, 0, 0);
const Pixel RED = Pixel(255, 0, 0);
const Pixel GREEN = Pixel(0, 255, 0);
const Pixel BLUE = Pixel(0, 0, 255);
const Pixel YELLOW = Pixel(255, 255, 0);
const Pixel CYAN = Pixel(0, 255, 255);
const Pixel MAGENTA = Pixel(255, 0, 255);
const Pixel ORANGE = Pixel(255, 165, 0);
const Pixel PURPLE = Pixel(128, 0, 128);
const Pixel BROWN = Pixel(165, 42, 42);
const Pixel GRAY = Pixel(128, 128, 128);
const Pixel LIGHT_GRAY = Pixel(200, 200, 200);
const Pixel DARK_GRAY = Pixel(50, 50, 50);
const Pixel PINK = Pixel(255, 192, 203);
const Pixel LIME = Pixel(128, 255, 0);
const Pixel TEAL = Pixel(0, 128, 128);
const Pixel NAVY = Pixel(0, 0, 128);
const Pixel MAROON = Pixel(128, 0, 0);
const Pixel OLIVE = Pixel(128, 128, 0);
const Pixel VIOLET = Pixel(128, 0, 128);
const Pixel INDIGO = Pixel(75, 0, 130);
const Pixel TURQUOISE = Pixel(64, 224, 208);
const Pixel CORAL = Pixel(255, 127, 80);
const Pixel CHOCOLATE = Pixel(210, 105, 30);
const Pixel SALMON = Pixel(250, 128, 114);
const Pixel GOLD = Pixel(255, 215, 0);
const Pixel SILVER = Pixel(192, 192, 192);
const Pixel BRONZE = Pixel(205, 127, 50);
const Pixel COPPER = Pixel(205, 127, 50);
const Pixel IRON = Pixel(192, 192, 192);
const Pixel STEEL = Pixel(192, 192, 192);
const Pixel TITANIUM = Pixel(192, 192, 192);
const Pixel PLATINUM = Pixel(192, 192, 192);



class Image{
    public:
        Image() : m_width(0), m_height(0) {}
        Image(unsigned int width, unsigned int height) : m_width(width), m_height(height) {
            if (width == 0 || height == 0) {
                throw invalid_argument("Image dimensions cannot be zero.");
            }
            m_pixels.resize(height, vector<Pixel>(width));
        }
        ~Image() {}

        void view(){
            save("image.ppm");
            system("magick convert image.ppm image.png > /dev/null 2>&1");
            system("chafa image.png");
            return;
        }

        unsigned int getWidth() const {
            return m_width;
        }
    
        unsigned int getHeight() const {
            return m_height;
        }

        Pixel getPixel(unsigned int x, unsigned int y) const {
            return m_pixels[y][x];
        }

        void setPixel(unsigned int x, unsigned int y, const Pixel& pixel) {
            m_pixels[y][x] = pixel;
        }

        void fillBox(unsigned int x1, unsigned int y1, unsigned int x2, unsigned int y2, const Pixel& pixel) {
            for (unsigned int y = y1; y <= y2; y++) {
                for (unsigned int x = x1; x <= x2; x++) {
                    setPixel(x, y, pixel);
                }
            }
        }

        // Fixed circle method - draws complete circle
        void fillCircle(unsigned int centerX, unsigned int centerY, unsigned int radius, const Pixel& pixel) {
            for (int dy = -(int)radius; dy <= (int)radius; dy++) {
                for (int dx = -(int)radius; dx <= (int)radius; dx++) {
                    if (dx*dx + dy*dy <= (int)(radius*radius)) {
                        int x = centerX + dx;
                        int y = centerY + dy;
                        if (x >= 0 && x < (int)m_width && y >= 0 && y < (int)m_height) {
                            m_pixels[y][x] = pixel;
                        }
                    }
                }
            }
        }

        
        void save(const string& filename) const {
            ofstream file(filename);
            if (!file.is_open()) {
                throw runtime_error("Could not open file for writing: " + filename);
            }
            file << "P3" << endl;
            file << m_width << " " << m_height << endl;
            file << "255" << endl;
            for (const auto& row : m_pixels) {
                for (const auto& pixel : row) {
                    file << pixel.red << " " << pixel.green << " " << pixel.blue << " ";
                }
                file << endl;
            }
        }

        void fill(const Pixel& pixel) {
            for (auto& row : m_pixels) {
                for (auto& p : row) {
                    p = pixel;
                }
            }
        }



    private:
        unsigned int m_width;
        unsigned int m_height;
        vector<vector<Pixel> > m_pixels;
};

int main(){
    Image image(100, 100);
    string command;
    int a;
    int b;
    int c;
    int d;
    Pixel color;
    int count = 0;
    
    while (true){
        cin >> command;
        if (command == "view"){
            cout << "d" << endl;
            image.view();
        }
        if (command=="test"){
            cout << "t" << endl;
        }
        command="";
        cout << count << endl;
        count++;
    }

    
    return 0;
}