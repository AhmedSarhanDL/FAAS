#!/usr/bin/env python3
import os
import sys
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file and return it as a string.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        doc.close()
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def save_text_to_file(text, output_path):
    """
    Save extracted text to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Error saving to {output_path}: {e}")
        return False

def convert_pdfs_in_directory(directory='.'):
    """
    Convert all PDF files in the specified directory to TXT files.
    """
    success_count = 0
    failure_count = 0
    
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
        
        print(f"Converting {pdf_file} to text...")
        text = extract_text_from_pdf(pdf_path)
        
        if text is not None:
            if save_text_to_file(text, txt_path):
                print(f"Successfully saved text to {txt_path}")
                success_count += 1
            else:
                failure_count += 1
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