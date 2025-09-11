#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <stdexcept>
#include <cstdlib>
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
            system("magick convert image.ppm image.png");
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

        // Fixed triangle method - uses barycentric coordinates
        void fillTriangle(unsigned int x1, unsigned int y1, unsigned int x2, unsigned int y2, 
                         unsigned int x3, unsigned int y3, const Pixel& pixel) {
            // Find bounding box manually (no C++11 required)
            int minX = (int)x1;
            if ((int)x2 < minX) minX = (int)x2;
            if ((int)x3 < minX) minX = (int)x3;
            
            int maxX = (int)x1;
            if ((int)x2 > maxX) maxX = (int)x2;
            if ((int)x3 > maxX) maxX = (int)x3;
            
            int minY = (int)y1;
            if ((int)y2 < minY) minY = (int)y2;
            if ((int)y3 < minY) minY = (int)y3;
            
            int maxY = (int)y1;
            if ((int)y2 > maxY) maxY = (int)y2;
            if ((int)y3 > maxY) maxY = (int)y3;
            
            // Clamp to image bounds
            if (minX < 0) minX = 0;
            if (maxX >= (int)m_width) maxX = (int)m_width - 1;
            if (minY < 0) minY = 0;
            if (maxY >= (int)m_height) maxY = (int)m_height - 1;
            
            // Check each pixel in bounding box
            for (int y = minY; y <= maxY; y++) {
                for (int x = minX; x <= maxX; x++) {
                    if (pointInTriangle(x, y, x1, y1, x2, y2, x3, y3)) {
                        m_pixels[y][x] = pixel;
                    }
                }
            }
        }

        bool pointInTriangle(int px, int py, int x1, int y1, int x2, int y2, int x3, int y3) {
            int denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3);
            if (denom == 0) return false;
            
            int a = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denom;
            int b = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denom;
            int c = 1 - a - b;
            
            return a >= 0 && b >= 0 && c >= 0;
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
    image.fill(Pixel(255, 0, 0));
    image.fillBox(20, 20, 60, 60, BLUE);
    image.view();
    
    return 0;
}
