import re
import sys

# CorpoLang to Python mappings (order matters for overlapping patterns)
MAPPINGS = [
    # Boolean literals (these need to be processed first)
    (r'is greenlit', 'True'),
    (r'is red-flagged', 'False'),
    
    # Arithmetic operations with nested assignments
    (r'Corporate will assign \'the combined efforts of (.*?) and (.*?)\'(,)? to (.*)', r'\4 = \1 + \2'),
    (r'Corporate will assign \'the removal of (.*?) off the (.*?) team\'(,)? to (.*)', r'\4 = \2 - \1'),
    (r'Corporate will assign \'the increased profitability of (.*?) by a factor of (.*?)\'(,)? to (.*)', r'\4 = \1 * \2'),
    (r'Corporate will assign \'the delegation of (.*?) tasks amongst the (.*?) teams\'(,)? to (.*)', r'\4 = \1 / \2'),
    (r'Corporate will assign \'the budget surplus left over from (.*?) after the (.*?) costs\'(,)? to (.*)', r'\4 = \1 % \2'),
    
    # Simple assignment
    (r'Corporate will assign \'(.*?)\'(,)? to (.*)', r'\3 = \1'),
    
    # Standalone arithmetic operations
    (r'the combined efforts of (.*?) and (.*?)', r'\1 + \2'),
    (r'the removal of (.*?) off the (.*?) team', r'\2 - \1'),
    (r'the increased profitability of (.*?) by a factor of (.*?)', r'\1 * \2'),
    (r'the delegation of (.*?) tasks amongst the (.*?) teams', r'\1 / \2'),
    (r'the budget surplus left over from (.*?) after the (.*?) costs', r'\1 % \2'),
    
    # Comparisons
    (r'(.*?) is in alignment with (.*?)', r'\1 == \2'),
    (r'(.*?) is in misalignment with (.*?)', r'\1 != \2'),
    (r'(.*?) is of lesser priority than (.*?)', r'\1 < \2'),
    (r'(.*?) is of greater priority than (.*?)', r'\1 > \2'),
    
    # Logical operators
    (r'both "(.*?)" and "(.*?)" are check-marked prerequisites', r'(\1) and (\2)'),
    (r'either "(.*?)" or "(.*?)" are check-marked prerequisites', r'(\1) or (\2)'),
    (r'(.*?) is not check-marked', r'not (\1)'),
    
    # Conditionals
    (r'In the case that \'(.*?)\'(,)?', r'if \1:'),
    (r'In the case that (.*)', r'if \1:'),  # Keep old pattern for backward compatibility
    (r'Alternatively, in the case that \'(.*?)\'(,)?', r'elif \1:'),
    (r'Alternatively, in the case that (.*)', r'elif \1:'),  # Keep old pattern for backward compatibility
    (r'Otherwise, let\'s pivot to', r'else:'),
    
    # Loops
    (r'We\'ll circle back (.*?) times in (.*)', r'for _ in range(\1):'),
    (r'While we\'re on the topic of \'(.*?)\'(,)?', r'while \1:'),
    (r'While we\'re on the topic of (.*)', r'while \1:'),  # Keep old pattern for backward compatibility
    
    # Loop control
    (r'then we\'ll move the meeting to the next touchpoint', r'break'),
    (r'then we\'ll circle back', r'continue'),
    
    # Function definition
    (r'This project, (.*?), will have the following deliverables: (.*)', r'def \1(\2):'),
    (r'then we\'ll go live with the (.*)', r'return \1'),
    
    # Import
    (r'Let\'s leverage (.*?) moving forward for this project', r'import \1'),
    
    # Print and Input
    (r'I\'ll ping "(.*?)" to your Slack inbox', r'print("\1")'),
    (r'I\'ll ping (.*?) to your Slack inbox', r'print(\1)'),
    (r'any input you have regarding (.*)', r'input(\1)'),
    
    # List literal
    (r'the inventory containing \((.*?)\)', r'[\1]'),
    
    # Comment
    (r'sidenote: (.*)', r'# \1')
]

def translate_corporlang_to_python(corporlang_code):
    """Convert CorpoLang code to Python."""
    python_code = corporlang_code
    
    # Apply each mapping pattern
    for pattern, replacement in MAPPINGS:
        python_code = re.sub(pattern, replacement, python_code, flags=re.MULTILINE)
    
    # Additional processing for loop indices - convert _ to loop variable
    python_code = re.sub(r'for _ in range\((.*?)\):', r'for i in range(\1):', python_code)
    python_code = re.sub(r'inventory_list\[_\]', r'inventory_list[i]', python_code)
    
    # Fix problem with boolean literals in while conditions
    python_code = re.sub(r'while (.*?) (True|False):', r'while \1 == \2:', python_code)
    
    return python_code

def interpret_file(filename, debug=False):
    """Interpret a CorpoLang file."""
    try:
        with open(filename, 'r') as file:
            corporlang_code = file.read()
        
        # Convert CorpoLang to Python
        python_code = translate_corporlang_to_python(corporlang_code)
        
        # For debugging
        if debug:
            print("Translated Python code:")
            print(python_code)
            print("-" * 50)
        
        # Execute the Python code
        exec(python_code, {})
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <corporlang_file> [--debug]")
        sys.exit(1)
    
    debug_mode = '--debug' in sys.argv
    filename = sys.argv[1]
    
    interpret_file(filename, debug=debug_mode) 