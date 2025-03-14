# PDF to TXT Converter

This tool converts PDF files to plain text (TXT) files. It processes all PDF files in a specified directory and creates corresponding TXT files with the same base name.

## Requirements

- Python 3.6 or higher
- PyMuPDF (fitz) library

## Installation

1. Create a virtual environment (recommended):
   ```
   python3 -m venv pdf_env
   source pdf_env/bin/activate  # On Windows: pdf_env\Scripts\activate
   ```

2. Install the required package:
   ```
   pip install PyMuPDF
   ```

## Usage

### Basic Usage

Run the script to convert all PDF files in the current directory:

```
./pdf_to_txt.py
```

### Specify a Directory

You can specify a directory containing PDF files:

```
./pdf_to_txt.py /path/to/pdf/files
```

### Output

For each PDF file processed, a corresponding TXT file will be created in the same directory. For example:
- `document.pdf` → `document.txt`
- `report.pdf` → `report.txt`

## Sample Files

The repository includes scripts to create sample PDF files for testing:

- `create_sample_pdf.py`: Creates a single sample PDF file
- `create_multiple_pdfs.py`: Creates multiple sample PDF files

## How It Works

The script uses PyMuPDF to extract text from each page of the PDF files and combines them into a single text file. It preserves the line breaks from the original PDF. 