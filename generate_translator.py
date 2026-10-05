```python
import sys
from pathlib import Path

functions = """# This program was created for the English Spelling Society,
# at the request of David Clyde Walters.
# It was created to make it easier to make custom translators for the society.
# It can be used to create both conservative and radical translators,
# depending on the needs of the user.
# It is, however, not affiliated with the English Spelling Society in any way.

# This is free and unencumbered software released into the public domain.

print("This translator script was created by the program generate_translator.py by Karsten Yawney")
text = input("Enter the text to be translated: ")
"""

have_file = input("Do you have a translator file? (y/n): ")

if have_file.lower().strip() != "y":
    print("\nPlease create a translator file with the following format:")
    print("lower")
    print("old new\n")
    print("For example, to replace 'hello' with 'hi', write:")
    print("hello hi")
    print("To convert all text to lowercase, write:")
    print("lower")
    print("Note: Replacing is case-sensitive, so 'Hello' and 'hello' are different.")
    print("You can have multiple replacement lines, and they will be applied in order.")
    print("\nIf you have suggestions, contact Karsten Yawney at karstenyawney@gmail.com")
    sys.exit()

# Clean up input path (removes quotes added by drag-and-drop in terminals)
rule_path_input = input(
    "Enter the path to the translator file: "
).strip("'\" ")

rule_path = Path(rule_path_input)

if not rule_path.is_file():
    print(f"Error: Could not find file at '{rule_path}'")
    sys.exit(1)

with open(rule_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line_number, line in enumerate(lines, start=1):
    clean_line = line.strip()

    # Ignore blank lines
    if not clean_line:
        continue

    if clean_line == "lower":
        functions += "text = text.lower()\n"
        continue

    # Rule format:
    # old new
    #
    # Split only on the first space so that the replacement can contain spaces.
    if " " not in clean_line:
        print(
            f"Warning: Ignoring invalid rule on line {line_number}: "
            f"{clean_line!r}"
        )
        continue

    old_str, new_str = clean_line.split(" ", 1)

    old_str = old_str.strip()
    new_str = new_str.strip()

    if not old_str:
        print(
            f"Warning: Ignoring rule with empty old text "
            f"on line {line_number}."
        )
        continue

    # repr() safely escapes quotes and special characters.
    functions += f"text = text.replace({old_str!r}, {new_str!r})\n"

functions += "print(text)\n"

# Handle saving the generated script
out_path_input = input(
    "Enter path to save the translator script "
    "[default: Desktop/translator.py]: "
).strip("'\" ")

if out_path_input:
    out_path = Path(out_path_input)
else:
    out_path = Path.home() / "Desktop" / "translator.py"

# Ensure output directory exists before writing
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, "w", encoding="utf-8") as file:
    file.write(functions)

print(f"\nSuccess! Translator program generated at: {out_path}")
```
