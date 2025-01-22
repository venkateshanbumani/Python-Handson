import random

def pick_any (name):
    if not name:
        return "Name can't be empty"
   
    print (f"This is the name: {name}")
    letter = input ("Pick one letter from the name:")
   
    if letter in name and len(letter) == 1:
        return f"you picket the letter {letter}"
    else:
        return ("Invalid input")

name = input ("Enter the name:").strip()
result = pick_any(name)
print (result)
