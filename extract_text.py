#!/usr/bin/env python3
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_path):
    """
    Extract text from a PDF file and save it to a text file.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            # Try a different extraction mode - "blocks" might work better for structured text
            text += page.get_text("text")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Successfully extracted text from {pdf_path} to {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return False

if __name__ == "__main__":
    pdf_path = "el_tor_circular_economy/output/el_tor_circular_economy_en.pdf"
    output_path = "el_tor_circular_economy/output/el_tor_circular_economy_en_pymupdf.txt"
    extract_text_from_pdf(pdf_path, output_path) 