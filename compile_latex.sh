#!/bin/bash

# Change to the el_tor_circular_economy directory
cd el_tor_circular_economy

# Create a temporary Dockerfile
cat > Dockerfile << 'EOF'
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-lang-arabic \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir
EOF

# Build the Docker image
docker build -t latex-compiler .

# Compile the English document
echo "Compiling main.tex..."
docker run --rm -v $(pwd):/workdir latex-compiler xelatex main.tex

# Compile the Arabic document
echo "Compiling main_ar.tex..."
docker run --rm -v $(pwd):/workdir latex-compiler xelatex main_ar.tex

# Clean up
rm Dockerfile

echo "Compilation completed. Check for main.pdf and main_ar.pdf in the el_tor_circular_economy directory." 