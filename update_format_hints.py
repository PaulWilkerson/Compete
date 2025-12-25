#!/usr/bin/env python3
"""
Script to update all format hints in challenge description files
to use generic placeholders instead of answer-revealing examples.
"""

import re
import os

def update_file(file_path):
    """Update format hints in a single file."""
    print(f"\nProcessing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Replace "Format: flag{...}" with generic version
        # But preserve the actual flag lines (they start with 'flag': 'flag{')
        # We only want to replace format hints in descriptions
        
        # Count occurrences before
        format_count = len(re.findall(r"Format: flag\{[^}]+\}", content))
        example_count = len(re.findall(r"Example format: flag\{[^}]+\}", content))
        
        # Replace Format: flag{...} patterns in description strings only
        # Look for patterns that are NOT in the actual flag definition line
        content = re.sub(
            r"(\s+)(Format|Example format): flag\{[^}]+\}(''')",
            r"\1Flag format: flag{your_answer_here}\3",
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ Updated {format_count + example_count} format hints")
            return True
        else:
            print(f"  - No changes needed")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main function to process all challenge files."""
    base_dir = "/workspaces/Compete/Compete"
    
    files_to_update = [
        os.path.join(base_dir, "cli/management/commands/populate_cli_challenges.py"),
        os.path.join(base_dir, "programming/management/commands/populate_programming_challenges.py"),
        os.path.join(base_dir, "cyber/management/commands/populate_cyber_challenges.py"),
    ]
    
    updated_count = 0
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_file(file_path):
                updated_count += 1
        else:
            print(f"\n✗ File not found: {file_path}")
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully updated {updated_count} of {len(files_to_update)} files")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
