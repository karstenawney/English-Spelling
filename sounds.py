print ("There are 26 letters  in english")
print ("They are split into vowels and consonants")
print ("Vowels: aeiou(y)")
print ("Consonants: bcdfghjklmnpqrstvwx(y)z")
print ("There are 39 phonemes in english")
print ("They are also split into vowels and consonants")
print ("Vowels are split into 3 groups: Short, Long and Gliding")
print ()
print ("Short vowels:")
print ("/a/ as in cat")
print ("/e/ as in get")
print ("/i/ as in sit")
print ("/o/ as in hot")
print ("/u/ as in cup")
print ()
print ("Long vowels:")
print ("/a:/ as in face")
print ("/e:/ as in see")
print ("/i:/ as in price")
print ("/o:/ as in boat")
print ("/u:/ as in cute")
print ()
print ("Gliding Vowels (R-defined):")
print ("/ar/ as in car")
print ("/ear/ as in near")
print ("/ir/ as in bird")
print ("/oy/ as in boy")
print ("/oo/ as in food")
print ("/ou/ as in mouth")
print ("/ur/ as in pure")
print ()
print ("Consonants are split into 5 groups: Plosives, Affricates, Fricates, Nasals and Approximates")
print ()
print ("Plosives: /p/, /b/, /t/, /d/, /k/, /g/")
print ("Affricates: /ch/, /j/")
print ("Fricatives: /f/, /v/, /th/, /s/, /z/, /sh/, /sz/, /h/")
print ("Nasals: /m/, /n/, /ng/")
print ("Approximants: /l/, /r/, /w/")
print ()
print ("This translator is meant to get rid of all silent letters, and to make english spell like it sounds")
print ("It does this by translating the words into sounds, and then translating the sounds into words")

vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"

text = input("Enter text to translate: ")
text = text.lower()
words = text.split()
text = text.replace("ui", "oo")
sounds = []
for word in words:
    sound = []
    previous_letter = "\0"
    while len(word) > 0:
        if word[0] in vowels:
            if word[0:3] == "ear":
                sound.append("/ear/")
                previous_letter = word[2:3]
                word = word[3:]
            elif word[1:2] == "r":
                sound.append(f"/{word[0]}r/")
                previous_letter = word[1:2]
                word = word[2:]
            elif word[:2] == "oy":
                sound.append("/oy/")
                previous_letter = word[1:2]
                word = word[2:]
            elif word[:2] == "oo":
                sound.append("/oo/")
                previous_letter = word[1:2]
                word = word[2:]
            elif word[:2] == "ou":
                sound.append("/ou/")
                previous_letter = word[1:2]
                word = word[2:]
            else:
                if ((previous_letter in consonants and word[1:2] in consonants) or (word[1:2] in consonants and word[1:2] == word[2:3]) or (word[1:3] == "ck") or (word[1:4] == "tch")):
                    sound.append(f"/{word[0]}/")
                    previous_letter = word[0]
                    word = word[1:]
                elif word[0] in vowels and word[1:2] in vowels:
                    sound.append(f"/{word[0]}:/")
                    sound.append(f"/{word[1:2]}/")
                    previous_letter = word[1:2]
                    word = word[2:]
                else:
                    sound.append(f"/{word[0]}:/")
                    previous_letter = word[0]
                    word = word[1:]
        else:
            # consonants
            if word.startswith("sh"):
                sound.append("/sh/")
                previous_letter = "h"
                word = word[2:]
            elif word.startswith("th"):
                sound.append("/th/")
                previous_letter = "h"
                word = word[2:]
            elif word.startswith("ng"):
                sound.append("/ng/")
                previous_letter = "g"
                word = word[2:]
            elif word.startswith("ch"):
                sound.append("/ch/")
                previous_letter = "h"
                word = word[2:]
            elif word[0] == "s":
                if sound and sound[-1] in ["/p/", "/t/", "/k/", "/f/", "/th/"]:
                    sound.append("/s/")
                    previous_letter = "s"
                    word = word[1:]
                else:
                    sound.append("/sz/")
                    previous_letter = "s"
                    word = word[1:]
            elif word[0] in "pbtdkgjfvszhmnlrw":
                sound.append(f"/{word[0]}/")
                previous_letter = word[0]
                word = word[1:]
            else:
                print (f"ERROR: character {word[0]} has no sound, skipping")
                sound.append(word[0])
                previous_letter = word[0]
                word = word[1:]
    sounds.append(sound)

print (sounds)
