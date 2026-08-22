# Backend Generator
import os
import sys

BASE_DIR = r'C:\Users\Master_Manu\.gemini\antigravity\scratch\codementor-ai\backend'

def write_module(rel_path, code):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as out:
        out.write(code.strip() + '\n')
    print(f'Wrote: {rel_path}')

print('Script generator initialized.')
