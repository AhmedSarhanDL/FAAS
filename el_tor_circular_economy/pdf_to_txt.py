#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def check_pdftotext():
    """
    Check if pdftotext is installed.
    """
    return shutil.which("pdftotext") is not None

def extract_text_with_pdftotext(pdf_path, output_path, is_arabic=False):
    """
    Extract text from a PDF file using pdftotext command-line tool.
    This generally handles Arabic text better than PyMuPDF.
    """
    try:
        # Set encoding options for all text
        encoding_option = "-enc UTF-8"
        
        # Use consistent options for both Arabic and English files
        # Raw mode often works better for multilingual documents
        layout_option = "-raw"
        eol_option = "-eol unix"  # Consistent line endings
        
        cmd = f"pdftotext {encoding_option} {layout_option} {eol_option} \"{pdf_path}\" \"{output_path}\""
        
        # Execute the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running pdftotext: {result.stderr}")
            return False
        
        # For Arabic documents, we need to fix the text direction
        if is_arabic:
            # Read the extracted text
            with open(output_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Add RTL mark at the beginning of each line for proper display
            lines = text.split('\n')
            rtl_lines = ['\u200F' + line for line in lines]  # U+200F is the RTL mark
            rtl_text = '\n'.join(rtl_lines)
            
            # Write back the modified text
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rtl_text)
        
        return True
    except Exception as e:
        print(f"Error processing {pdf_path} with pdftotext: {e}")
        return False

def convert_pdfs_in_directory(directory='.'):
    """
    Convert all PDF files in the specified directory to TXT files.
    """
    success_count = 0
    failure_count = 0
    
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
        txt_path = os.path.join(directory, os.path.splitext(pdf_file)[0] + '.txt')
        
        # Determine if this is an Arabic document based on filename
        is_arabic = "_ar." in pdf_file
        
        print(f"Converting {pdf_file} to text...")
        if is_arabic:
            print(f"Detected Arabic document: {pdf_file}")
        
        if extract_text_with_pdftotext(pdf_path, txt_path, is_arabic):
            print(f"Successfully saved text to {txt_path}")
            success_count += 1
        else:
            failure_count += 1
    
    print(f"\nConversion complete: {success_count} successful, {failure_count} failed")

if __name__ == "__main__":
    # If a directory is provided as a command-line argument, use it
    # Otherwise, use the current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    convert_pdfs_in_directory(directory) 