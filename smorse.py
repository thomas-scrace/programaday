"""
https://www.reddit.com/r/dailyprogrammer/comments/cmd1hb/20190805_challenge_380_easy_smooshed_morse_code_1/

For the purpose of this challenge, Morse code represents every letter as a sequence of 1-4 characters, each of which is either . (dot) or - (dash). The code for the letter a is .-, for b is -..., etc. The codes for each letter a through z are:

.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..
Normally, you would indicate where one letter ends and the next begins, for instance with a space between the letters' codes, but for this challenge, just smoosh all the coded letters together into a single string consisting of only dashes and dots.

Examples
smorse("sos") => "...---..."
smorse("daily") => "-...-...-..-.--"
smorse("programmer") => ".--..-.-----..-..-----..-."
smorse("bits") => "-.....-..."
smorse("three") => "-.....-..."
An obvious problem with this system is that decoding is ambiguous. For instance, both bits and three encode to the same string, so you can't tell which one you would decode to without more information.

Optional bonus challenges
For these challenges, use the enable1 word list. It contains 172,823 words. If you encode them all, you would get a total of 2,499,157 dots and 1,565,081 dashes.

1. The sequence -...-....-.--. is the code for four different words (needing, nervate, niding, tiling). Find the only sequence that's the code for 13 different words.
2. autotomous encodes to .-..--------------..-..., which has 14 dashes in a row. Find the only word that has 15 dashes in a row.
3. Call a word perfectly balanced if its code has the same number of dots as dashes. counterdemonstrations is one of two 21-letter words that's perfectly balanced. Find the other one.
4. protectorate is 12 letters long and encodes to .--..-.----.-.-.----.-..--., which is a palindrome (i.e. the string is the same when reversed). Find the only 13-letter word that encodes to a palindrome.
5. --.---.---.-- is one of five 13-character sequences that does not appear in the encoding of any word. Find the other four.
"""
import collections
import itertools
import string

import requests


morse = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split(
    " "
)
morse = {string.ascii_lowercase[i]: morse[i] for i in range(26)}


def smorse(s):
    return "".join([morse[c] for c in s])


assert smorse("sos") == "...---..."
assert smorse("daily") == "-...-...-..-.--"
assert smorse("programmer") == ".--..-.-----..-..-----..-."
assert smorse("bits") == "-.....-..."
assert smorse("three") == "-.....-..."

words = requests.get(
    "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
).content.split()

sequence_counts = collections.defaultdict(int)

thirteen_character_sequences = ["".join(p) for p in itertools.product(["-", "."], repeat=13)]

for w in words:
    w = str(w, "utf-8")
    seq = smorse(w)
    fifteen = "-" * 15
    if fifteen in seq:
        print(f"The word with 15 dashes in a row is {w}")
    sequence_counts[seq] += 1
    if sequence_counts[seq] == 13:
        print(f"The only sequence that is the code for 13 differnent words is {seq}")
    if len(w) == 21:
        if seq.count("-") == seq.count("."):
            if w != "counterdemonstrations":
                print(f"The only perfectly balanced 21 letter word that is not counterdemonstrations is {w}")
    if len(w) == 13:
        if seq == ''.join(reversed(seq)):
            print(f"The only 13-letter word that encodes to a palindrome is {w}")
    remove = []
    for thirteen in thirteen_character_sequences:
        if thirteen in seq:
            remove.append(thirteen)
    for r in remove:
        thirteen_character_sequences.remove(r)

print(f"The five 13-character sequences that do not appear in the encoding of any word are: {thirteen_character_sequences}")


