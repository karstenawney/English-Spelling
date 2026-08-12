import sys
from pathlib import Path

functions = """# This program was created for the english spelling society, 
# at the request of David Clyde Walters. 
# It was created to make it easier to make custom translators for the society.
# It can be used to create both conservative and radical translators, depending on the needs of the user.
# It is, however, not affiliated with the english spelling society in any way.

# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# You can find more information about The Unlicense at https://unlicense.org/


print("This translator script was created by the program generate_translator.py by Karsten Yawney")
text = input("Enter the text to be translated: ")
"""

have_file = input("Do you have a translator file? (y/n): ")

if have_file.lower().strip() != 'y':
    print("\nPlease create a translator file with the following format:")
    print("lower")
    print("replace(old, new)\n")
    print("For example, to replace 'hello' with 'hi', write:")
    print("replace(hello, hi)")
    print("To convert all text to lowercase, write:")
    print("lower")
    print("Note: Replacing is case-sensitive, so 'Hello' and 'hello' are different.")
    print("You can have multiple replace() lines, and they will be applied in order.")
    print("\nIf you have suggestions, contact Karsten Yawney at karstenyawney@gmail.com")
    sys.exit()

# Clean up input path (removes quotes added by drag-and-drop in terminals)
rule_path_input = input("Enter the path to the translator file: ").strip("'\" ")
rule_path = Path(rule_path_input)

if not rule_path.is_file():
    print(f"Error: Could not find file at '{rule_path}'")
    sys.exit(1)

with open(rule_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for line in lines:
    clean_line = line.strip()
    
    if clean_line == "lower":
        functions += "text = text.lower()\n"
        
    elif clean_line.startswith("replace(") and clean_line.endswith(")"):
        # Extract content between replace( and )
        args = clean_line[8:-1]
        
        # Split on the first comma found
        if "," in args:
            old_str, new_str = args.split(",", 1)
            old_str = old_str.strip()
            new_str = new_str.strip()
            
            # Using repr() automatically escapes internal quotes safely!
            functions += f"text = text.replace({repr(old_str)}, {repr(new_str)})\n"

functions += "print(text)\n"

# Handle saving the generated script
out_path_input = input("Enter path to save the translator script [default: Desktop/translator.py]: ").strip("'\" ")

if out_path_input:
    out_path = Path(out_path_input)
else:
    out_path = Path.home() / "Desktop" / "translator.py"

# Ensure output directory exists before writing
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as file:
    file.write(functions)

print(f"\nSuccess! Translator program generated at: {out_path}")