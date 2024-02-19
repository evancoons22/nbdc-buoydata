#include <iostream>
#include "eccodes.h"

int main(int argc, char** argv) {
    // Check for the correct usage
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <grib_file_path>" << std::endl;
        return 1;
    }

    const char* filename = argv[1];
    FILE* in = fopen(filename, "rb");

    if (!in) {
        std::cerr << "Could not open file: " << filename << std::endl;
        return 1;
    }

    int err = 0;
    codes_handle* h = nullptr;

    // Loop over all the GRIB messages
    while ((h = codes_handle_new_from_file(nullptr, in, PRODUCT_GRIB, &err)) != nullptr) {
        if (err != CODES_SUCCESS) {
            codes_handle_delete(h);
            continue;
        }

        // Example: Get some metadata from the GRIB message
        long paramId;
        codes_get_long(h, "paramId", &paramId);
        std::cout << "Parameter ID: " << paramId << std::endl;

        // Clean up
        codes_handle_delete(h);
    }

    fclose(in);

    return 0;
}

