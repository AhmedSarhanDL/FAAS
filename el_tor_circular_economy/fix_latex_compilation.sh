#!/bin/bash

# Script to fix LaTeX encoding issues and recompile documents
# This script applies the fix_latex_encoding.py and fix_arabic_commands.py scripts to all LaTeX files
# and then recompiles the documents using the compile_docker.sh script

echo "====================================================="
echo "  El Tor Circular Economy - LaTeX Encoding Fix & Compilation"
echo "====================================================="

# Make the Python scripts executable
chmod +x fix_latex_encoding.py
chmod +x fix_arabic_commands.py

# Fix LaTeX encoding in all files
echo ""
echo "Fixing LaTeX encoding issues in all files..."
python3 fix_latex_encoding.py --directory . --recursive

# Check if the fix was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to fix LaTeX encoding issues"
    exit 1
fi

# Fix Arabic commands in all files
echo ""
echo "Fixing Arabic commands in all files..."
python3 fix_arabic_commands.py --directory . --recursive

# Check if the fix was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to fix Arabic commands"
    exit 1
fi

echo ""
echo "====================================================="
echo "  Starting LaTeX Compilation"
echo "====================================================="

# Run the compile_docker.sh script
./compile_docker.sh

echo ""
echo "====================================================="
echo "  Process Complete"
echo "====================================================="
echo ""
echo "If the compilation was successful, the fixed PDFs should be in the output directory."
echo "You can check them with:"
echo "  - output/el_tor_circular_economy_en.pdf (English version)"
echo "  - output/el_tor_circular_economy_ar.pdf (Arabic version)"
echo ""

# List the output files
ls -lh output/ 