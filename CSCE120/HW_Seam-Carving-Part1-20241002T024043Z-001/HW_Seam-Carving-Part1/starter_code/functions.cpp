#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
#include "functions.h"

using std::cout, std::endl, std::string;

void initializeImage(Pixel image[][MAX_HEIGHT]) {
  for (unsigned int col = 0; col < MAX_WIDTH; col++) {
    for (unsigned int row = 0; row < MAX_HEIGHT; row++) {
      image[col][row] = {0, 0, 0};
    }
  }
}

void loadImage(string filename, Pixel image[][MAX_HEIGHT], unsigned int& width, unsigned int& height) {
  // TODO: implement (part 1)
  std::ifstream file(filename);

    if (!file.is_open()) {
        throw std::runtime_error("Failed to open " + filename);
    }

    string type;
    file >> type;

    // check PPM type
    if (type != "P3" && type != "p3") {
        throw std::runtime_error("Invalid type " + type);
    }

    file >> width >> height;
    if (width <= 0 || height <= 0 || width > MAX_WIDTH || height > MAX_HEIGHT) {
        throw std::runtime_error("Invalid dimensions");
    }
    
    int maxColorValue;
    file >> maxColorValue;
    if (maxColorValue != 255) {
        throw std::runtime_error("Invalid max color value");
    }

    unsigned int pixelCount = 0;
    for (unsigned int row = 0; row < height; ++row) {
        for (unsigned int col = 0; col < width; ++col) {
            short r, g, b;
            if (!(file >> r >> g >> b)) {
                throw std::runtime_error("Not enough values");
            }

            if (r < 0 || r >= 256 || g < 0 || g >= 256 || b < 0 || b >= 256) {
                throw std::runtime_error("Invalid color value");
            }

            image[col][row] = { r, g, b };
            ++pixelCount;
        }
    }

    // Check if there are too many pixel values
    int extra;
    if (file >> extra) {
        throw std::runtime_error("Too many values");
    }
}

void outputImage(string filename, Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height) {
  // TODO: implement (part 1)
  
    std::ofstream ofs(filename);
    if (!ofs) {
        throw std::runtime_error("Failed to open " + filename);
    }
    
    
    ofs << "P3\n";            
    ofs << width << " " << height << "\n";   
    ofs << "255\n";           
    
    
    for (unsigned int row = 0; row < height; ++row) {
        for (unsigned int col = 0; col < width; ++col) {
            Pixel& p = image[col][row];
            ofs << p.r << " " << p.g << " " << p.b << " ";
        }
        ofs << "\n";  
    }
}

unsigned int energy(Pixel image[][MAX_HEIGHT], unsigned int x, unsigned int y, unsigned int width, unsigned int height) {
  // TODO: implement (part 1)
    int Rx = image[(x + 1) % width][y].r - image[(x - 1 + width) % width][y].r;   // Using wrapping for the left-right
    int Gx = image[(x + 1) % width][y].g - image[(x - 1 + width) % width][y].g;
    int Bx = image[(x + 1) % width][y].b - image[(x - 1 + width) % width][y].b;

    unsigned int deltaX2 = Rx * Rx + Gx * Gx + Bx * Bx;

    
    int Ry = image[x][(y + 1) % height].r - image[x][(y - 1 + height) % height].r;   // Using wrapping for the top-bottom
    int Gy = image[x][(y + 1) % height].g - image[x][(y - 1 + height) % height].g;
    int By = image[x][(y + 1) % height].b - image[x][(y - 1 + height) % height].b;

    unsigned int deltaY2 = Ry * Ry + Gy * Gy + By * By;

    
    unsigned int energy = deltaX2 + deltaY2;

    return energy;
}

// uncomment functions as you implement them (part 2)

unsigned int loadVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int start_col, 
                              unsigned int width, unsigned int height, unsigned int seam[]) {
    unsigned int total_energy = 0;

    // Initialize seam starting from the given column in the first row
    seam[0] = start_col;
    total_energy += energy(image, start_col, 0, width, height);

    // Traverse through the rows, starting from row 1
    for (unsigned int row = 1; row < height; ++row) {
        unsigned int col = seam[row - 1];  // Get the column from the previous row

        // Initialize minimum energy values
        unsigned int min_col = col; // Start with the current column
        unsigned int min_energy = energy(image, col, row, width, height);
        unsigned int left_energy = min_energy + 1;

        // Check right neighbor (if available)
        if (col < width - 1) {
            unsigned int right_energy = energy(image, col + 1, row, width, height);
            // Only consider right if it has strictly less energy than current minimum
            if (right_energy < min_energy) {
                min_energy = right_energy;
                min_col = col + 1; // Move to right column
                
            }
        }

        // Check left neighbor (if available)
        if (col > 0) {
            left_energy = energy(image, col - 1, row, width, height);
            // If left energy is less or equal to the current minimum
            if (left_energy < min_energy) {
                min_energy = left_energy;
                min_col = col - 1; // Move to left column
            }
            
        }

        // Update seam for the current row and accumulate energy
        seam[row] = min_col;
        total_energy += min_energy;
    }

    return total_energy;  // Return the total energy of the seam
}

unsigned int loadHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int start_row, 
                                unsigned int width, unsigned int height, unsigned int seam[]) {
    unsigned int total_energy = 0;  // Total energy of the horizontal seam

    // Initialize the first column's row index based on start_row
    seam[0] = start_row;
    total_energy += energy(image, 0, start_row, width, height);

    // Traverse each column, finding the minimum energy in neighboring pixels
    for (unsigned int col = 1; col < width; ++col) {
        unsigned int row = seam[col - 1];  // The row from the previous column

        // Check for boundary conditions: above, center, below
        unsigned int min_row = row;  // The row with the minimum energy in this column
        unsigned int min_energy = energy(image, col, row, width, height);

        // Check the above neighbor, if it exists
        if (row > 0) {
            unsigned int above_energy = energy(image, col, row - 1, width, height);
            if (above_energy < min_energy) {
                min_energy = above_energy;
                min_row = row - 1;
            }
        }

        // Check the below neighbor, if it exists
        if (row < height - 1) {
            unsigned int below_energy = energy(image, col, row + 1, width, height);
            if (below_energy < min_energy) {
                min_energy = below_energy;
                min_row = row + 1;
            }
        }

        // Update seam for the current column and accumulate total energy
        seam[col] = min_row;
        total_energy += min_energy;
    }

    return total_energy;  // Return the total energy of the seam
}

void findMinVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height, unsigned int seam[]) {
    unsigned int min_energy = ~0U;  // Set to the maximum possible unsigned integer using bitwise NOT
    unsigned int temp_seam[MAX_HEIGHT];  // Temporary array for current seam

    // Iterate over all possible starting columns
    for (unsigned int col = 0; col < width; ++col) {
        unsigned int current_energy = loadVerticalSeam(image, col, width, height, temp_seam);

        // Update if the current seam has less energy
        if (current_energy < min_energy) {
            min_energy = current_energy;

            // Copy the current seam to the result seam
            for (unsigned int row = 0; row < height; ++row) {
                seam[row] = temp_seam[row];
            }
        }
    }
}

void findMinHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height, unsigned int seam[]) {
    unsigned int min_energy = ~0U;  // Set to the maximum possible unsigned integer using bitwise NOT
    unsigned int temp_seam[MAX_WIDTH];  // Temporary array for current seam

    // Iterate over all possible starting rows
    for (unsigned int row = 0; row < height; ++row) {
        unsigned int current_energy = loadHorizontalSeam(image, row, width, height, temp_seam);

        // Update if the current seam has less energy
        if (current_energy < min_energy) {
            min_energy = current_energy;

            // Copy the current seam to the result seam
            for (unsigned int col = 0; col < width; ++col) {
                seam[col] = temp_seam[col];
            }
        }
    }
}

void removeVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int& width, unsigned int height, const unsigned int verticalSeam[]) {
    // Loop through each row to remove the pixel at the seam position
    for (unsigned int row = 0; row < height; ++row) {
        unsigned int seam_col = verticalSeam[row];  // Get the column index of the seam for the current row
        
        // Shift all pixels to the left starting from the seam column
        for (unsigned int col = seam_col; col < width - 1; ++col) {
            image[col][row] = image[col + 1][row];  // Shift pixels to the left
        }
    }

    // Decrease the image width by 1 since we removed one column
    width--;
}

void removeHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int& height, const unsigned int horizontalSeam[]) {
    // Loop through each column to remove the pixel at the seam position
    for (unsigned int col = 0; col < width; ++col) {
        unsigned int seam_row = horizontalSeam[col];  // Get the row index of the seam for the current column
        
        // Shift all pixels upwards starting from the seam row
        for (unsigned int row = seam_row; row < height - 1; ++row) {
            image[col][row] = image[col][row + 1];  // Shift pixels upwards
        }
    }

    // Decrease the image height by 1 since we removed one row
    height--;
}
