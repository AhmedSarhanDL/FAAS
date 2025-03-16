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

# Add a timeout to prevent hanging
TIMEOUT_DURATION=1200  # 20 minutes timeout (increased from 10 minutes)

# Check if timeout command is available
if command -v timeout &> /dev/null; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout &> /dev/null; then
    TIMEOUT_CMD="gtimeout"
else
    echo "⚠️ Neither 'timeout' nor 'gtimeout' command found. Running without timeout protection."
    echo "   Consider installing coreutils package for timeout functionality:"
    echo "   brew install coreutils"
    TIMEOUT_CMD=""
fi

# Function to check for missing files
check_missing_files() {
    local missing_files=0
    
    # Check for critical files
    if [ ! -f "main.tex" ]; then
        echo "✗ Critical file missing: main.tex"
        missing_files=1
    fi
    
    if [ ! -f "main_ar.tex" ]; then
        echo "✗ Critical file missing: main_ar.tex"
        missing_files=1
    fi
    
    if [ ! -f "missing_labels.tex" ]; then
        echo "✗ Critical file missing: missing_labels.tex"
        missing_files=1
    fi
    
    # Check for shared documents
    if [ ! -f "shared_documents/site_master_plan.tex" ]; then
        echo "⚠️ Warning: shared_documents/site_master_plan.tex is missing"
    fi
    
    if [ ! -f "shared_documents/site_master_plan_ar.tex" ]; then
        echo "⚠️ Warning: shared_documents/site_master_plan_ar.tex is missing"
    fi
    
    if [ ! -f "shared_documents/water_management_plan.tex" ]; then
        echo "⚠️ Warning: shared_documents/water_management_plan.tex is missing"
    fi
    
    if [ ! -f "shared_documents/water_management_plan_ar.tex" ]; then
        echo "⚠️ Warning: shared_documents/water_management_plan_ar.tex is missing"
    fi
    
    return $missing_files
}

# Check for missing files before compilation
echo "Checking for critical files..."
check_missing_files
if [ $? -eq 1 ]; then
    echo "✗ Critical files are missing. Please check the error messages above."
    echo "  Attempting to continue anyway..."
fi

# Compile English version
echo ""
echo "===== COMPILING ENGLISH VERSION ====="
echo "Compiling main.tex using xelatex with timeout of ${TIMEOUT_DURATION} seconds..."

# Create a temporary file to capture the log
touch compile.log

# Run xelatex with timeout if available
if [ -n "$TIMEOUT_CMD" ]; then
    $TIMEOUT_CMD $TIMEOUT_DURATION docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
        echo 'Running first pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex > compile.log 2>&1 && \
        echo 'Running second pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex >> compile.log 2>&1 && \
        echo 'Running final pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex >> compile.log 2>&1"
    TIMEOUT_STATUS=$?
else
    docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
        echo 'Running first pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex > compile.log 2>&1 && \
        echo 'Running second pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex >> compile.log 2>&1 && \
        echo 'Running final pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main.tex >> compile.log 2>&1"
    TIMEOUT_STATUS=$?
fi

# Check if compilation was successful or timed out
if [ -n "$TIMEOUT_CMD" ] && [ $TIMEOUT_STATUS -eq 124 ]; then
    echo "✗ Compilation timed out after ${TIMEOUT_DURATION} seconds. Check for errors in compile.log"
    echo "  Particularly check tables in financial_plan.tex for formatting issues."
    # Continue with the script
elif [ -f "main.pdf" ]; then
    # Make a backup copy of the English PDF in case the move fails
    cp "main.pdf" "main_backup.pdf"
    # Move the PDF to the output directory
    mv "main.pdf" "output/el_tor_circular_economy_en.pdf"
    echo "✓ Successfully created output/el_tor_circular_economy_en.pdf"
    # Verify the file exists in the output directory
    if [ -f "output/el_tor_circular_economy_en.pdf" ]; then
        echo "✓ Verified English PDF exists in output directory"
    else
        # If move failed, use the backup
        if [ -f "main_backup.pdf" ]; then
            cp "main_backup.pdf" "output/el_tor_circular_economy_en.pdf"
            echo "✓ Used backup to create output/el_tor_circular_economy_en.pdf"
            rm "main_backup.pdf"
        else
            echo "✗ Failed to save English PDF to output directory"
        fi
    fi
else
    echo "✗ Failed to compile main.tex with xelatex"
    echo "  Check LaTeX errors in compile.log"
    # Display the last few lines of the log file
    echo "Last 20 lines of compile.log:"
    tail -n 20 compile.log
fi

# Compile Arabic version
echo ""
echo "===== COMPILING ARABIC VERSION ====="
echo "Compiling main_ar.tex using xelatex with timeout of ${TIMEOUT_DURATION} seconds..."

# Run xelatex with timeout if available
if [ -n "$TIMEOUT_CMD" ]; then
    $TIMEOUT_CMD $TIMEOUT_DURATION docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
        echo 'Running first pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex > compile_ar.log 2>&1 && \
        echo 'Running second pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex >> compile_ar.log 2>&1 && \
        echo 'Running final pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex >> compile_ar.log 2>&1"
    TIMEOUT_STATUS=$?
else
    docker run --rm -v "$CURRENT_DIR:/workdir" $DOCKER_IMAGE sh -c "cd /workdir && \
        echo 'Running first pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex > compile_ar.log 2>&1 && \
        echo 'Running second pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex >> compile_ar.log 2>&1 && \
        echo 'Running final pass...' && \
        xelatex -interaction=nonstopmode -halt-on-error main_ar.tex >> compile_ar.log 2>&1"
    TIMEOUT_STATUS=$?
fi

# Check if compilation was successful or timed out
if [ -n "$TIMEOUT_CMD" ] && [ $TIMEOUT_STATUS -eq 124 ]; then
    echo "✗ Compilation of Arabic version timed out after ${TIMEOUT_DURATION} seconds."
    echo "  Check for errors in compile_ar.log"
    # Display the last few lines of the log file
    echo "Last 20 lines of compile_ar.log:"
    tail -n 20 compile_ar.log
elif [ -f "main_ar.pdf" ]; then
    # Make a backup copy of the Arabic PDF in case the move fails
    cp "main_ar.pdf" "main_ar_backup.pdf"
    # Move the PDF to the output directory
    mv "main_ar.pdf" "output/el_tor_circular_economy_ar.pdf"
    echo "✓ Successfully created output/el_tor_circular_economy_ar.pdf"
    # Verify the file exists in the output directory
    if [ -f "output/el_tor_circular_economy_ar.pdf" ]; then
        echo "✓ Verified Arabic PDF exists in output directory"
        # Check if the file has a table of contents
        if pdftotext -f 2 -l 2 "output/el_tor_circular_economy_ar.pdf" - | grep -q "محتويات"; then
            echo "✓ Table of contents found in Arabic PDF"
        else
            echo "⚠️ Table of contents may be missing or incomplete in Arabic PDF"
            echo "  This is normal if this is the first compilation. Run the script again if needed."
        fi
    else
        # If move failed, use the backup
        if [ -f "main_ar_backup.pdf" ]; then
            cp "main_ar_backup.pdf" "output/el_tor_circular_economy_ar.pdf"
            echo "✓ Used backup to create output/el_tor_circular_economy_ar.pdf"
            rm "main_ar_backup.pdf"
        else
            echo "✗ Failed to save Arabic PDF to output directory"
        fi
    fi
else
    echo "✗ Failed to compile main_ar.tex"
    echo "  Check LaTeX errors in compile_ar.log"
    # Display the last few lines of the log file
    echo "Last 20 lines of compile_ar.log:"
    tail -n 20 compile_ar.log
fi

# Clean up auxiliary files but preserve log files
echo ""
echo "Cleaning up auxiliary files..."
# Save compile logs if they exist and are not empty
if [ -s "compile.log" ]; then
    cp compile.log compile.log.backup
fi
if [ -s "compile_ar.log" ]; then
    cp compile_ar.log compile_ar.log.backup
fi

# Remove auxiliary files but not log files
rm -f *.aux *.out *.toc *.lof *.lot *.bbl *.blg *.nav *.snm *.vrb

# Restore compile logs if they were backed up
if [ -f "compile.log.backup" ]; then
    mv compile.log.backup compile.log
    echo "✓ Preserved compile.log"
fi
if [ -f "compile_ar.log.backup" ]; then
    mv compile_ar.log.backup compile_ar.log
    echo "✓ Preserved compile_ar.log"
fi

echo ""
echo "====================================================="
echo "  Compilation Complete"
echo "====================================================="
echo ""
echo "Output files can be found in the 'output' directory:"
echo "  - output/el_tor_circular_economy_en.pdf (English version)"
echo "  - output/el_tor_circular_economy_ar.pdf (Arabic version)"
echo ""
echo "If the table of contents is still empty, run this script again."
echo "LaTeX typically needs multiple compilation runs to generate a complete TOC."
echo ""
ls -lh output/
echo ""
echo "Done!"