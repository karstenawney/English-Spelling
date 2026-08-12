import re

def split_into_syllables(word: str) -> list[str]:
    """Splits an English word into a list of syllables using rule-based regular expressions."""
    # Convert to lowercase for uniform processing
    word_lower = word.lower()
    
    # Handle short words or edge cases immediately
    if len(word_lower) <= 3:
        return [word]
        
    # Step 1: Define vowel groups (including vowel teams like 'ee', 'ou', 'ai')
    # Treat 'y' as a vowel if it doesn't start the word
    vowel_pattern = r'[aeiouy]+'
    
    # Step 2: Extract all vowel sounds and their start/end indices
    vowel_spans = [match.span() for match in re.finditer(vowel_pattern, word_lower)]
    
    # If 1 or 0 vowel groups found, it's a single syllable word
    if len(vowel_spans) <= 1:
        return [word]
        
    # Adjust for silent 'e' at the end of a word (e.g., 'table' vs 'cake')
    # 'le' counts as a syllable, but a trailing silent 'e' alone does not
    if word_lower.endswith('e') and not word_lower.endswith('le'):
        # Check if there are other vowels before it
        if len(vowel_spans) > 1:
            vowel_spans.pop() # Remove the silent e from syllable count
            
    if len(vowel_spans) <= 1:
        return [word]

    split_indices = []
    
    # Step 3: Iterate through pairs of consecutive vowel groups to find where to split
    for i in range(len(vowel_spans) - 1):
        current_vowel_end = vowel_spans[i][1]
        next_vowel_start = vowel_spans[i+1][0]
        
        # Get the intervening consonants between the two vowel groups
        consonants_between = word_lower[current_vowel_end:next_vowel_start]
        num_consonants = len(consonants_between)
        
        if num_consonants == 0:
            # V/V pattern (e.g., 'li-on', 'po-et') -> split between them
            split_point = current_vowel_end
        elif num_consonants == 1:
            # V/CV pattern (e.g., 'ba-by') -> split before the consonant
            split_point = current_vowel_end
        elif num_consonants >= 2:
            # VC/CV pattern (e.g., 'nap-kin', 're-pro-gram-ming')
            # Split right down the middle of the consonants
            split_point = current_vowel_end + (num_consonants // 2)
            
        split_indices.append(split_point)

    # Step 4: Reconstruct the word into a list using the identified split points
    syllables = []
    start_idx = 0
    for split_point in split_indices:
        # Match case mapping to keep the original capitalization intact
        syllables.append(word[start_idx:split_point])
        start_idx = split_point
    syllables.append(word[start_idx:])
    
    return syllables

text = input("Enter text: ")
#words = text.split(" ,.;'\"()\n\r\t\f1234567890!@#$%^&*_+-=<>?/\\|`~[]{}")
words = text.split()
streaming = []
for word in words:
    syllables = split_into_syllables(word)
    print(f"{word}: {syllables}")
    streaming += syllables + ["|"]
print (streaming)
text = ""
for syllable in streaming:
    text += syllable + " "
print (text)