INTRO = """There are 26 letters in English.
They are split into vowels and consonants.
Vowels: aeiou(y)
Consonants: bcdfghjklmnpqrstvwx(y)z
There are 40 phonemes in English.
They are also split into vowels and consonants.
Vowels are split into 4 groups: Short, Long, R-defined and Gliding.

Short vowels:
(a) as in cat
(e) as in get
(i) as in sit
(o) as in hot
(u) as in cup

Long vowels:
(à) as in face
(è) as in see
(ì) as in price
(ò) as in boat
(ù) as in cute

R-defined:
(a*) as in car
(e*) as in err
(i*) as in bird
(o*) as in origin
(u*) as in pure

Gliding vowels:
(èar) as in near
(oy) as in boy
(oo) as in food
(ow) as in cow or mouth

Consonants are split into 5 groups: Plosives, Affricates, Fricatives, Nasals and Approximants.

Plosives: (p), (b), (t), (d), (k), (g)
Affricates: (ch), (j)
Fricatives: (f), (v), (th), (s), (z), (sh), (h)
Nasals: (m), (n), (ng)
Approximants: (l), (r), (w), (y)

This translator gets rid of silent letters and makes English spell like it sounds.
It does this by translating words into sounds, and then translating the sounds back into words.
"""

VOWELS = "aeiou"
VOICELESS = {"(p)", "(t)", "(k)", "(f)", "(th)"}
SIBILANTS = {"(s)", "(z)", "(sh)", "(ch)", "(j)"}

# Common words that don't follow the rules
EXCEPTIONS = {
    "the": ["(th)", "(u)"],
    "a": ["(u)"],
    "of": ["(o)", "(v)"],
    "to": ["(t)", "(oo)"],
    "do": ["(d)", "(oo)"],
    "you": ["(y)", "(oo)"],
    "was": ["(w)", "(o)", "(z)"],
    "one": ["(w)", "(u)", "(n)"],
    "said": ["(s)", "(e)", "(d)"],
}

# Letter groups that make one sound, checked in order
CLUSTERS = [
    ("tch", "(ch)"), ("dge", "(j)"), ("sh", "(sh)"), ("th", "(th)"),
    ("ng", "(ng)"), ("ch", "(ch)"), ("ph", "(f)"), ("ck", "(k)"),
    ("wh", "(w)"), ("ss", "(s)"),
]
# Only at the start of a word (silent first letter)
INITIAL_CLUSTERS = [("kn", "(n)"), ("wr", "(r)"), ("gn", "(n)")]

# How each sound is written when we turn sounds back into text
RESPELL = {
    "(a:)": "à", "(e:)": "è", "(i:)": "ì", "(o:)": "ò", "(u:)": "ù",
    "(a*)": "ar", "(e*)": "er", "(i*)": "ir", "(o*)": "or", "(u*)": "ur",
    "(ear)": "èar",
}


def is_vowel(ch):
    # Careful: "" in "aeiou" is True in Python, so check the length too
    return len(ch) == 1 and ch in VOWELS


def vowel_sounds(word):
    """Work out the sound of the vowel at the start of word.
    Returns (list of sounds, number of letters used)."""
    v = word[0]
    two = word[:2]

    # Special combinations first
    if word[:3] == "ear":
        return ["(ear)"], 3
    if two == "oy":
        return ["(oy)"], 2
    if two in ("oo", "ui"):
        return ["(oo)"], 2
    if two in ("ou", "ow"):
        return ["(ow)"], 2
    if two == "ew":
        return ["(u:)"], 2
    if two == "ay":
        return ["(a:)"], 2

    # R-defined: vowel + r, as long as the r isn't starting a new syllable
    if word[1:2] == "r" and not is_vowel(word[2:3]):
        return [f"({v}*)"], 2

    # Two vowels together: the first is long, the second is dropped
    if is_vowel(word[1:2]):
        return [f"({v}:)"], 2

    # Single vowel: long or short?
    rest = word[1:]
    if rest == "":                                   # open syllable (go, he, no)
        return [f"({v}:)"], 1
    if len(rest) >= 2 and not is_vowel(rest[0]) and rest[1] == "e" and rest[2:] in ("", "s", "d"):
        return [f"({v}:)"], 1                        # magic e (make, hope, makes)
    if len(rest) >= 2 and not is_vowel(rest[0]) and (is_vowel(rest[1]) or rest[1] == "y"):
        return [f"({v}:)"], 1                        # vowel-consonant-vowel (paper, baby)
    return [f"({v})"], 1                             # closed syllable (cat, bed, lunch)


def consonant_sounds(word, sound):
    """Work out the sound of the consonant at the start of word.
    Returns (list of sounds, number of letters used)."""
    for letters, phoneme in CLUSTERS:
        if word.startswith(letters):
            return [phoneme], len(letters)
    if not sound:
        for letters, phoneme in INITIAL_CLUSTERS:
            if word.startswith(letters):
                return [phoneme], len(letters)
    if word == "mb":                                 # lamb, thumb
        return ["(m)"], 2

    ch = word[0]
    if word[1:2] == ch:                              # double letter (bell, happy): sound it once
        return [], 1
    if ch == "s":
        if not sound or sound[-1] in VOICELESS:
            return ["(s)"], 1
        return ["(z)"], 1
    if ch == "c":
        return (["(s)"] if word[1:2] and word[1:2] in "eiy" else ["(k)"]), 1
    if ch == "x":
        return ["(k)", "(s)"], 1
    if ch == "q":
        return ["(k)"], 1
    if ch == "y":
        return ["(y)"], 1
    if ch in "pbtdkgjfvzhmnlrw":
        return [f"({ch})"], 1
    return [ch], 1                                   # digits, punctuation: pass through


def word_to_sounds(word):
    word = word.replace("qu", "kw")
    if word in EXCEPTIONS:
        return list(EXCEPTIONS[word])

    sound = []
    has_vowel = False
    while word:
        ch = word[0]

        # Silent e: final "e", or "es"/"ed" endings that don't add a syllable
        if has_vowel and sound:
            if word == "e":
                word = word[1:]
                continue
            if word == "es" and sound[-1] not in SIBILANTS:
                word = word[1:]
                continue
            if word == "ed" and sound[-1] not in ("(t)", "(d)"):
                word = word[1:]
                continue

        if ch == "y" and (sound or not is_vowel(word[1:2])):
            # y acting as a vowel
            if len(word) == 1:
                sound.append("(e:)" if has_vowel else "(i:)")   # happy / my
            else:
                sound.append("(i)")                              # gym
            has_vowel = True
            word = word[1:]
        elif is_vowel(ch):
            phonemes, used = vowel_sounds(word)
            sound += phonemes
            has_vowel = True
            word = word[used:]
        else:
            phonemes, used = consonant_sounds(word, sound)
            sound += phonemes
            word = word[used:]
    return sound


def sounds_to_text(sound):
    return "".join(RESPELL.get(s, s.strip("()")) for s in sound)


def main():
    print(INTRO)
    while True:
        text = input("Enter text to translate (blank to quit): ").lower().strip()
        if not text:
            break
        sounds = [word_to_sounds(w) for w in text.split()]
        print(sounds)
        print(" ".join("".join(s) for s in sounds))
        print(" ".join(sounds_to_text(s) for s in sounds))
        print()


if __name__ == "__main__":
    main()
