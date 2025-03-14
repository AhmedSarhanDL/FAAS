#!/bin/bash

# Script to compile all LaTeX files for El Tor Circular Economy project using Docker
# This script compiles both English and Arabic versions of the documentation

echo "====================================================="
echo "  El Tor Circular Economy - Docker LaTeX Compilation"
echo "====================================================="

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker first:"
    echo "  Visit: https://docs.docker.com/get-docker/"
    exit 1
else
    echo "✓ Docker found: $(command -v docker)"
fi

# Create output directory for PDFs if it doesn't exist
mkdir -p output

# Get the absolute path of the current directory
CURRENT_DIR=$(pwd)

echo ""
echo "Starting compilation process using Docker..."
echo ""

# Using a more reliable image for Arabic support
DOCKER_IMAGE="registry.gitlab.com/islandoftex/images/texlive:latest"

echo "Pulling LaTeX Docker image (this may take a while the first time)..."
docker pull $DOCKER_IMAGE

# Compile English version
echo ""
echo "===== COMPILING ENGLISH VERSION ====="
echo "Compiling main.tex using pdflatex..."

docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
    pdflatex -interaction=nonstopmode main.tex && \
    pdflatex -interaction=nonstopmode main.tex"

# Check if PDF was created
if [ -f "main.pdf" ]; then
    mv "main.pdf" "output/el_tor_circular_economy_en.pdf"
    echo "✓ Successfully created output/el_tor_circular_economy_en.pdf"
else
    echo "✗ Failed to compile main.tex"
fi

# Compile Arabic version
echo ""
echo "===== COMPILING ARABIC VERSION ====="
echo "Compiling main_ar.tex using xelatex..."

docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
    xelatex -interaction=nonstopmode main_ar.tex && \
    xelatex -interaction=nonstopmode main_ar.tex"

# Check if PDF was created
if [ -f "main_ar.pdf" ]; then
    mv "main_ar.pdf" "output/el_tor_circular_economy_ar.pdf"
    echo "✓ Successfully created output/el_tor_circular_economy_ar.pdf"
else
    echo "✗ Failed to compile main_ar.tex"
fi

# Clean up auxiliary files
echo ""
echo "Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.nav *.snm *.vrb

echo ""
echo "====================================================="
echo "  Compilation Complete"
echo "====================================================="
echo ""
echo "Output files can be found in the 'output' directory:"
echo "  - output/el_tor_circular_economy_en.pdf (English version)"
echo "  - output/el_tor_circular_economy_ar.pdf (Arabic version)"
echo ""

# List the output files
ls -lh output/

echo ""
echo "Testing PDF files with pdf_to_txt.py..."
if [ -f "pdf_to_txt.py" ]; then
    chmod +x pdf_to_txt.py
    ./pdf_to_txt.py output/
    
    # Display first few lines of the text files to verify content
    if [ -f "output/el_tor_circular_economy_en.txt" ]; then
        echo ""
        echo "First 10 lines of English text file:"
        head -n 10 output/el_tor_circular_economy_en.txt
    fi
    
    if [ -f "output/el_tor_circular_economy_ar.txt" ]; then
        echo ""
        echo "First 10 lines of Arabic text file:"
        head -n 10 output/el_tor_circular_economy_ar.txt
    fi
else
    echo "pdf_to_txt.py not found in current directory. Please run it manually."
fi

echo ""
echo "Done!"