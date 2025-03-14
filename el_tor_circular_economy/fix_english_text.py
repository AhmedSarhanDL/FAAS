#!/usr/bin/env python3
import os
import re
import sys

def is_english_line(line):
    """
    Check if a line contains primarily English text.
    Returns True for English text, False for Arabic or other non-Latin text.
    """
    # Check if line contains any English letters
    english_pattern = re.compile(r'[a-zA-Z]')
    has_english = bool(english_pattern.search(line))
    
    # Check if line contains Arabic characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    has_arabic = bool(arabic_pattern.search(line))
    
    # If line has English letters and no Arabic, consider it English
    if has_english and not has_arabic:
        return True
    
    # If line has numbers, punctuation, or special characters but no Arabic, keep it
    if not has_arabic and any(c.isdigit() or c in '.,;:!?-_()[]{}• ' for c in line):
        return True
    
    return False

def fix_english_text_file(input_path, output_path):
    """
    Fix the English text file by removing Arabic text and keeping only English text.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter out Arabic lines
        english_lines = []
        for line in lines:
            # Keep empty lines
            if not line.strip():
                english_lines.append(line)
                continue
            
            # Keep English lines
            if is_english_line(line):
                english_lines.append(line)
        
        # Write the fixed content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(english_lines)
        
        print(f"Successfully fixed English text file: {output_path}")
        return True
    
    except Exception as e:
        print(f"Error fixing English text file: {e}")
        return False

def main():
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python fix_english_text.py <input_file> [output_file]")
        print("If output_file is not provided, input_file will be overwritten.")
        return
    
    input_path = sys.argv[1]
    
    # If output file is not provided, use the input file
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # Create a backup of the original file
        backup_path = input_path + ".bak"
        try:
            with open(input_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"Created backup of original file: {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
            return
        
        output_path = input_path
    
    # Fix the English text file
    fix_english_text_file(input_path, output_path)

if __name__ == "__main__":
    main() 