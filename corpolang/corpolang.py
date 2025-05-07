#!/usr/bin/env python3
import sys
import os
import argparse

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the interpreter
from interpreter import interpret_file

def main():
    parser = argparse.ArgumentParser(description='CorpoLang Interpreter')
    parser.add_argument('file', help='CorpoLang file to interpret')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    interpret_file(args.file, debug=args.debug)

if __name__ == "__main__":
    main() 