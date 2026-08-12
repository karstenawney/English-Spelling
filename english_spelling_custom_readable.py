print ("There are 26 letters in the english language")
print ("There are 44 sounds in the english language")
print ("There are 197 letter combinations that make a sound that can be represented by one letter.")
print ("Ex: letter: f, sound code: /f/, letter combination: gh, ph, ff, lf, ft")
print ("This script takes text as an input, tries to convert it into sound codes. \n" \
       "Then it prints the simplified letters")


def sound(a, b):
    global text
    result = []
    insound = False
    i = 0
    lena = len(a)
    
    while i < len(text):
        # Toggle 'insound' when hitting a slash
        if text[i] == '(' or text[i] == ')':
            insound = not insound
            result.append(text[i])
            i += 1
        # If outside slashes and matching string 'a'
        elif not insound and text[i:i + lena] == a:
            result.append(b)
            i += lena  # Skip past the matched substring
        else:
            result.append(text[i])
            i += 1
    text = "".join(result)

text = input("Enter text: ").lower()


def syllabify():
    sound("ngue", "(ŋ)")
    sound("gue", "(g)")
    sound("dge", "(j)")
    sound("th", "(þ)")
    sound("bb", "(b)")
    sound("dd", "(d)")
    sound("ed", "(d)")
    sound("ff", "(f)")
    sound("ph", "(f)")
    sound("gh", "(f)")
    sound("lf", "(f)")
    sound("ft", "(f)")
    sound("gg", "(g)")
    sound("gh", "(g)")
    sound("gu", "(g)")
    sound("wh", "(h)")
    sound("ge", "(j)")
    sound("di", "(j)")
    sound("gg", "(j)")
    sound("qu", "(k)")
    sound("ch", "(k)")
    sound("cc", "(k)")
    sound("lk", "(k)")
    sound("ck", "(k)")
    sound("ll", "(l)")
    sound("mm", "(m)")
    sound("mb", "(m)")
    sound("mn", "(m)")
    sound("lm", "(m)")
    sound("nn", "(n)")
    sound("kn", "(n)")
    sound("gn", "(n)")
    sound("pn", "(n)")
    sound("pp", "(p)")
    sound("rr", "(r)")
    sound("wr", "(r)")
    sound("rh", "(r)")
    sound("ss", "(s)")
    sound("sc", "(s)")
    sound("ps", "(s)")
    sound("st", "(s)")
    sound("tt", "(t)")
    sound("ve", "(v)")
    sound("x", "(k)")

    sound("aa", "(a)")
    sound("ee", "(e)")
    sound("ii", "(i)")
    sound("oo", "(o)")

def letters():
    global text
    insound = False
    end = len(text)
    i = 0
    while i < end:
        if text[i] == '(' or text[i] == ')':
            insound = not insound
        elif not insound:
            if text[i] in "bcdfghjklmnpqrstvwxzy":
                text = text[:i] + "(" + text[i] + ")" + text[i + 1:]
                i += 2  # Skip past the newly added slashes
                end += 2  # Adjust the end index due to the added characters
        i += 1

import re

def capitalize_long_vowels(text: str) -> str:
    # Step 1: Normalize the entire string to lowercase
    text = text.lower()
    
    # Step 2: Define regex patterns for common long vowel rules
    # Pattern 1: Vowel-Consonant-Silent 'e' (e.g., m-a-k-e, l-i-k-e)
    # Uses a lookahead assertion (?=[a-z]e\b) to find the vowel but only capitalize the first one
    def vce_replace(match):
        vowel, consonant, e = match.group(1), match.group(2), match.group(3)
        return f"{vowel.upper()}{consonant}{e}"
    
    text = re.sub(r'([aeiou])([bcdfghjklmnpqrstvwxyz])(e\b)', vce_replace, text)
    
    # Pattern 2: Common Vowel Teams (e.g., ai, ay, ee, ea, oa, oe)
    # The first vowel is long (capitalized), and the second is silent (kept lowercase)
    vowel_teams = {
        'ai': 'Ai', 'ay': 'Ay', 
        'ee': 'Ee', 'ea': 'Ea', 
        'ie': 'Ie',
        'oa': 'Oa', 'oe': 'Oe', 'ow': 'Ow'
    }
    for team, replacement in vowel_teams.items():
        text = text.replace(team, replacement)
        
    # Pattern 3: Single open-syllable or standalone pronoun words (e.g., "I", "go", "be", "me")
    text = re.sub(r'\b(i)\b', 'I', text)
    text = re.sub(r'\b(g|n|s)(o)\b', lambda m: f"{m.group(1)}{m.group(2).upper()}", text)
    text = re.sub(r'\b(b|m|h|w)(e)\b', lambda m: f"{m.group(1)}{m.group(2).upper()}", text)

    return text


print (f"Preprocessed: {text}")
syllabify()
print (f"Letter Pair Sounds: {text}")
letters()
print (f"Consonant Sounds: {text}")
text = capitalize_long_vowels(text)
print (f"Vowels: {text}")
text = text.replace("(", "").replace(")", "")
print (f"Final: {text}")