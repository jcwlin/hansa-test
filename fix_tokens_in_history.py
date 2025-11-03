#!/usr/bin/env python3
"""
Script to fix tokens count in existing history records
"""
import pickle
import os
import logging

def estimate_tokens_from_data(history_entry):
    """Estimate tokens based on available data"""
    # Basic estimation based on rows and columns
    rows = history_entry.get('rows', 0)
    cols = history_entry.get('cols', 0)
    files_count = len(history_entry.get('files', []))
    
    # Rough estimation:
    # - Each file processed: ~500-1000 tokens for analysis
    # - Each data row extracted: ~50-100 tokens
    # - Base overhead: ~200 tokens
    
    base_tokens = 200
    file_tokens = files_count * 750  # Average tokens per file
    data_tokens = rows * 75          # Average tokens per row
    
    estimated_tokens = base_tokens + file_tokens + data_tokens
    return max(estimated_tokens, 1)

def fix_history_tokens():
    """Fix tokens in history.pkl"""
    history_file = 'history.pkl'
    
    if not os.path.exists(history_file):
        print("No history.pkl file found")
        return
    
    # Load existing history
    with open(history_file, 'rb') as f:
        history = pickle.load(f)
    
    print(f"Found {len(history)} history records")
    
    updated_count = 0
    for entry in history:
        current_tokens = entry.get('tokens', 0)
        if current_tokens == 0:
            estimated_tokens = estimate_tokens_from_data(entry)
            entry['tokens'] = estimated_tokens
            updated_count += 1
            print(f"Updated tokens for {entry.get('time', 'unknown')}: {estimated_tokens}")
    
    if updated_count > 0:
        # Backup original file
        backup_file = 'history_backup.pkl'
        with open(backup_file, 'wb') as f:
            pickle.dump(history, f)
        print(f"Backup created: {backup_file}")
        
        # Save updated history
        with open(history_file, 'wb') as f:
            pickle.dump(history, f)
        print(f"Updated {updated_count} records in {history_file}")
    else:
        print("No records needed updating")

if __name__ == "__main__":
    fix_history_tokens()
