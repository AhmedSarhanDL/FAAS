#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import shutil

def check_pdftotext():
    """
    Check if pdftotext is installed.
    """
    return shutil.which("pdftotext") is not None

def is_arabic_text(text):
    """
    Check if text contains Arabic characters.
    """
    # Arabic Unicode range
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(arabic_pattern.search(text))

def is_latin_text(text):
    """
    Check if text contains Latin characters.
    """
    # Latin Unicode range (basic Latin, Latin-1 Supplement, Latin Extended)
    latin_pattern = re.compile(r'[a-zA-Z\u00C0-\u00FF\u0100-\u017F]')
    return bool(latin_pattern.search(text))

def extract_text_with_pdftotext(pdf_path, output_path, is_arabic=False):
    """
    Extract text from a PDF file using pdftotext command-line tool.
    """
    try:
        # Set encoding options
        encoding_option = "-enc UTF-8"
        
        # Additional options for better text extraction
        if is_arabic:
            # For Arabic documents
            layout_option = "-raw"  # Raw mode often works better for non-Latin scripts
            eol_option = "-eol unix"  # Consistent line endings
            cmd = f"pdftotext {encoding_option} {layout_option} {eol_option} \"{pdf_path}\" \"{output_path}\""
        else:
            # For English documents
            layout_option = "-layout"  # Maintain original layout
            cmd = f"pdftotext {encoding_option} {layout_option} \"{pdf_path}\" \"{output_path}\""
        
        # Execute the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running pdftotext: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error processing {pdf_path} with pdftotext: {e}")
        return False

def filter_text_by_language(input_path, output_path, keep_arabic=True):
    """
    Filter text file to keep only Arabic or only Latin text.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        filtered_lines = []
        for line in lines:
            # Skip empty lines
            if not line.strip():
                filtered_lines.append(line)
                continue
                
            is_arabic = is_arabic_text(line)
            is_latin = is_latin_text(line)
            
            # Keep line if it matches the desired language
            if (keep_arabic and is_arabic) or (not keep_arabic and is_latin):
                filtered_lines.append(line)
            # Keep lines with numbers and symbols but no letters
            elif not is_arabic and not is_latin and any(c.isdigit() or c in '.,;:!?-_()[]{}' for c in line):
                filtered_lines.append(line)
        
        # For Arabic text, add RTL mark at the beginning of each line
        if keep_arabic:
            filtered_lines = ['\u200F' + line if line.strip() else line for line in filtered_lines]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)
        
        return True
    except Exception as e:
        print(f"Error filtering {input_path}: {e}")
        return False

def process_pdf_files(directory='.'):
    """
    Process PDF files in the directory to create language-specific text files.
    """
    # Check if pdftotext is installed
    if not check_pdftotext():
        print("Error: pdftotext is not installed. Please install poppler-utils.")
        print("  For macOS: brew install poppler")
        print("  For Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("  For Fedora/RHEL/CentOS: sudo dnf install poppler-utils")
        return
    
    # Get all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return
    
    print(f"Found {len(pdf_files)} PDF files in {directory}")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        
        # Determine if this is an Arabic document based on filename
        is_arabic = "_ar." in pdf_file
        
        # Temporary text file
        temp_txt_path = os.path.join(directory, f"{base_name}_temp.txt")
        
        # Final text file
        txt_path = os.path.join(directory, f"{base_name}.txt")
        
        print(f"Processing {pdf_file}...")
        
        # Extract text from PDF
        if extract_text_with_pdftotext(pdf_path, temp_txt_path, is_arabic):
            # Filter text by language
            if filter_text_by_language(temp_txt_path, txt_path, keep_arabic=is_arabic):
                print(f"Successfully created language-specific text file: {txt_path}")
            else:
                print(f"Failed to filter text for {pdf_file}")
        else:
            print(f"Failed to extract text from {pdf_file}")
        
        # Clean up temporary file
        if os.path.exists(temp_txt_path):
            os.remove(temp_txt_path)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    # If a directory is provided as a command-line argument, use it
    # Otherwise, use the current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    process_pdf_files(directory) 