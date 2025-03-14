#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix Arabic Commands in LaTeX Files for El Tor Circular Economy Project

This script ensures that Arabic text is properly wrapped in \RL{} commands
for correct right-to-left rendering in LaTeX documents.
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

def is_already_wrapped(text):
    """Check if text is already wrapped in \RL{} command."""
    # Simple check for \RL{...} pattern
    return bool(re.match(r'^\s*\\RL\{.*\}\s*$', text))

def fix_arabic_commands(input_path, output_path=None):
    """
    Fix Arabic commands in LaTeX file by ensuring Arabic text is wrapped in \RL{} commands.
    
    Args:
        input_path: Path to the input LaTeX file
        output_path: Path to save the fixed file (if None, creates a backup and overwrites original)
    """
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} does not exist")
        return False
    
    # Skip non-Arabic files (those without _ar in the filename)
    if "_ar.tex" not in input_path and "main_ar.tex" not in input_path:
        print(f"Skipping non-Arabic file: {input_path}")
        return True
    
    # Create backup if no output path specified
    if output_path is None:
        backup_path = f"{input_path}.bak"
        shutil.copy2(input_path, backup_path)
        output_path = input_path
        print(f"Created backup at {backup_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
    
    # Fix Arabic commands
    fixed_content = []
    in_document = False
    in_command = False
    command_buffer = ""
    
    for line in content:
        # Track when we're inside the document environment
        if '\\begin{document}' in line:
            in_document = True
            fixed_content.append(line)
            continue
        elif '\\end{document}' in line:
            in_document = False
            fixed_content.append(line)
            continue
        
        # Skip preamble lines
        if not in_document:
            fixed_content.append(line)
            continue
        
        # Skip lines that are already in a command environment
        if line.strip().startswith('\\') and not line.strip().startswith('\\RL{'):
            fixed_content.append(line)
            continue
        
        # Skip empty or comment lines
        if not line.strip() or line.strip().startswith('%'):
            fixed_content.append(line)
            continue
        
        # Check if line contains Arabic text and is not already wrapped
        if is_arabic_text(line) and not is_already_wrapped(line):
            # Handle multi-line content
            if '{' in line and '}' not in line:
                in_command = True
                command_buffer = line
            else:
                # Wrap the line in \RL{} command
                wrapped_line = f"\\RL{{{line.strip()}}}\n"
                fixed_content.append(wrapped_line)
        elif in_command:
            # Continue collecting multi-line command
            command_buffer += line
            if '}' in line:
                in_command = False
                fixed_content.append(command_buffer)
                command_buffer = ""
        else:
            # No changes needed
            fixed_content.append(line)
    
    # Write fixed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_content)
    
    print(f"Fixed Arabic commands in {output_path}")
    return True

def fix_all_arabic_files(directory, recursive=True):
    """
    Fix Arabic commands in all LaTeX files in a directory.
    
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
    
    # Filter for Arabic files
    arabic_files = [f for f in tex_files if "_ar.tex" in str(f) or "main_ar.tex" in str(f)]
    
    print(f"Found {len(arabic_files)} Arabic LaTeX files")
    
    # Process each file
    for tex_file in arabic_files:
        file_path = str(tex_file)
        print(f"Processing {file_path}...")
        fix_arabic_commands(file_path)
    
    print("Finished processing all Arabic LaTeX files")

def main():
    parser = argparse.ArgumentParser(description="Fix Arabic commands in LaTeX files")
    parser.add_argument("--file", help="Path to a specific LaTeX file to fix")
    parser.add_argument("--output", help="Path to save the fixed file (only used with --file)")
    parser.add_argument("--directory", help="Directory containing LaTeX files to fix")
    parser.add_argument("--recursive", action="store_true", help="Search directory recursively")
    
    args = parser.parse_args()
    
    if args.file:
        fix_arabic_commands(args.file, args.output)
    elif args.directory:
        fix_all_arabic_files(args.directory, args.recursive)
    else:
        print("Error: Please specify either --file or --directory")
        parser.print_help()

if __name__ == "__main__":
    main() 