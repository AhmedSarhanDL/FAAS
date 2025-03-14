#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix LaTeX Encoding Issues for El Tor Circular Economy Project

This script helps fix encoding issues in LaTeX files by ensuring proper language separation
between Arabic and English content. It adds proper language environment tags where needed.
"""

import os
import re
import shutil
import argparse
from pathlib import Path

def is_arabic_text(text):
    """Check if text contains Arabic characters."""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def is_english_text(text):
    """Check if text contains primarily English/Latin characters."""
    # Remove LaTeX commands first
    text_without_commands = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', '', text)
    # Count English characters
    english_chars = len(re.findall(r'[a-zA-Z]', text_without_commands))
    # Count all characters (excluding whitespace)
    all_chars = len(re.sub(r'\s', '', text_without_commands))
    
    # If there are no characters, it's not English text
    if all_chars == 0:
        return False
    
    # If more than 60% of characters are English, consider it English text
    return english_chars / all_chars > 0.6

def fix_latex_file(input_path, output_path=None, is_arabic_main=False):
    """
    Fix LaTeX file by ensuring proper language environment tags.
    
    Args:
        input_path: Path to the input LaTeX file
        output_path: Path to save the fixed file (if None, creates a backup and overwrites original)
        is_arabic_main: Whether this is an Arabic main document (affects default language)
    """
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} does not exist")
        return False
    
    # Create backup if no output path specified
    if output_path is None:
        backup_path = f"{input_path}.bak"
        shutil.copy2(input_path, backup_path)
        output_path = input_path
        print(f"Created backup at {backup_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix language environments
    fixed_content = []
    in_document = False
    current_language = "arabic" if is_arabic_main else "english"
    
    for line in content.split('\n'):
        # Track when we're inside the document environment
        if '\\begin{document}' in line:
            in_document = True
        elif '\\end{document}' in line:
            in_document = False
        
        # Skip preamble lines
        if not in_document:
            fixed_content.append(line)
            continue
        
        # Check if line already has language environment
        if '\\begin{arabic}' in line or '\\end{arabic}' in line or '\\begin{english}' in line or '\\end{english}' in line:
            fixed_content.append(line)
            continue
            
        # Determine language of current line
        is_arabic = is_arabic_text(line)
        is_english = is_english_text(line)
        
        # Skip empty or special lines
        if not line.strip() or line.strip().startswith('%') or (not is_arabic and not is_english):
            fixed_content.append(line)
            continue
        
        # Add language environment if needed
        if is_arabic and current_language != "arabic":
            if current_language != "":
                fixed_content.append(f"\\end{{{current_language}}}")
            fixed_content.append("\\begin{arabic}")
            current_language = "arabic"
            fixed_content.append(line)
        elif is_english and current_language != "english":
            if current_language != "":
                fixed_content.append(f"\\end{{{current_language}}}")
            fixed_content.append("\\begin{english}")
            current_language = "english"
            fixed_content.append(line)
        else:
            # Same language, no change needed
            fixed_content.append(line)
    
    # Close any open language environment
    if in_document and current_language:
        fixed_content.append(f"\\end{{{current_language}}}")
    
    # Write fixed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_content))
    
    print(f"Fixed LaTeX file saved to {output_path}")
    return True

def fix_all_latex_files(directory, recursive=True):
    """
    Fix all LaTeX files in a directory.
    
    Args:
        directory: Directory containing LaTeX files
        recursive: Whether to search recursively
    """
    directory_path = Path(directory)
    
    # Find all .tex files
    if recursive:
        tex_files = list(directory_path.glob('**/*.tex'))
    else:
        tex_files = list(directory_path.glob('*.tex'))
    
    print(f"Found {len(tex_files)} LaTeX files")
    
    # Process each file
    for tex_file in tex_files:
        file_path = str(tex_file)
        print(f"Processing {file_path}...")
        
        # Determine if it's an Arabic main file
        is_arabic_main = "_ar.tex" in file_path or "main_ar.tex" in file_path
        
        # Fix the file
        fix_latex_file(file_path, is_arabic_main=is_arabic_main)
    
    print("Finished processing all LaTeX files")

def main():
    parser = argparse.ArgumentParser(description="Fix LaTeX encoding issues for El Tor Circular Economy Project")
    parser.add_argument("--file", help="Path to a specific LaTeX file to fix")
    parser.add_argument("--output", help="Path to save the fixed file (only used with --file)")
    parser.add_argument("--directory", help="Directory containing LaTeX files to fix")
    parser.add_argument("--recursive", action="store_true", help="Search directory recursively")
    parser.add_argument("--arabic", action="store_true", help="Treat as Arabic main document")
    
    args = parser.parse_args()
    
    if args.file:
        fix_latex_file(args.file, args.output, args.arabic)
    elif args.directory:
        fix_all_latex_files(args.directory, args.recursive)
    else:
        print("Error: Please specify either --file or --directory")
        parser.print_help()

if __name__ == "__main__":
    main() 