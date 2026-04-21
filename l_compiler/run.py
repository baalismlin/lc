#!/usr/bin/env python3
"""
python -m l_compiler.cli input.l output.py
"""

import sys
import logging

from l_compiler import compile_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    if len(sys.argv) != 3:
        print('usage: python run.py <input.l> <output.py>')
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        compile_file(input_path, output_path)
    except FileNotFoundError as e:
        print(f'file not found: {e}')
        sys.exit(1)
    except SyntaxError as e:
        print(f'syntax error: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
