# Ideograph Cipher - ideoCipher.py - Proof of concept by Jigsy (https://github.com/Jigsy1) released under the Unlicense.
#
# How to use:
# ---------------
# print(ideoEncode("Hello!"))
# print(ideoDecode("償禮幇 凉杞釧 櫛禪滲 峻狛桶哩悸傳鳩檜裡 曉峨嶺焙祐蕪廟鮫結"))
#
# string = "This is demonstrating encoding a string from a variable."
# print(ideoEncode(string))
#
# Tweaking:
# ----------
# If you wish to change which number reflects which character, edit CharOrder under [Settings] in the Ideo.ini file. E.g.
#
# [Settings]
# CharOrder=!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
#
# ...becomes...
#
# CharOrder=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/\()[]{}!?+-=%#"'`$&*,.:;<>@^_|~
#
# If you wish to add more characters, add the character to the end of the CharOrder under the [Settings] section and add the
# number for that character. So for example, £ onto the current charset would become 94=<ideographs>.
#
# You will need at least two ideographs because of the "no dopplegänger" code.
#
# If you want to encrypt spaces, add Space=<ideographs> under the [Key] section. Again, you will need at least two ideographs.
#
# If you want to pad the message with ideographs that have no value, add Padding=<ideographs> under the [Key] section.
#
# And again, you will need at least two ideographs.
#

import os
import re
import secrets


# define(s):

IDEO_INI = "Ideo.ini"

CIPHER_TABLE = {}
FIRST_PADDING_CHANCE = 100000
SECOND_PADDING_CHANCE = 1.29
# `-> For calculating how many times a padding character should appear. Feel free to change these.

NEWLINE_REGEX = r"[\n\r]+"
# `-> For splitting on main().


# Function(s):

def findInTable(character):
    """Find the key of a character within the CIPHER_TABLE."""
    for key, value in CIPHER_TABLE.items():
        if key == "CharOrder":
            continue
        if character in value:
            return key
    return False

def isCipherKey(keyName):
    """Check if a key is defined in the CIPHER_TABLE."""
    try:
        CIPHER_TABLE[keyName]
    except KeyError:
        return False
    return True

def ideoDecode(string):
    """Decode a string encoded with ideoCipher."""
    char = 0
    output = ""
    while char < len(string):
        if string[char] == " " or string[char] == " ":
            # `-> The first is a space - ASCII=32; the other is an emulated space from mIRC - ASCII=160.
            output = output + " "
            char += 1
            continue
        result = findInTable(string[char])
        if result != False:
            if result == "Space":
                output = output + " "
                char += 1
                continue
            if result != "Padding":
                # ¦-> Assuming the result isn't Padding, find the ideograph and convert it to a comprehensible value.
                # `-> E.g. 醉 => 77 => m
                output = output + CIPHER_TABLE["CharOrder"][int(result)]
        char += 1
    return output
    # `-> Return the output.

def ideoEncode(string):
    """Encode a string with ideoCipher."""
    char = 0
    output = ""
    lastChar = ""
    while char < len(string):
        if string[char] in CIPHER_TABLE["CharOrder"]:
            # `-> Check the character via the acceptable characters as defined in CharOrder.
            match = CIPHER_TABLE["CharOrder"].rfind(string[char])
            # `-> Convert the character to a number. E.g. ! = 0, " = 1, | = 91, etc.
            ideos = CIPHER_TABLE[str(match)]
            ideos = ideos.replace(lastChar, "", 1)
            # `-> Get all the ideographs we can use, minus the one we used last. (Doesn't matter if lastChar is NULL here.)
            current = ideos[secrets.choice(range(0, len(ideos)))]
            # `-> Now get a random ideograph from the ones we can use.
            output = output + current
            # `-> And then add it to the output string.
            lastChar = current
            # ¦-> Set the last character to the new ideograph.
            # ¦-> The reason for this is to make sure the ideograph can never be used again in succession. For example, Grrr => 貌よ一よ
            # ¦-> is acceptable, whilst Grrr => 貌よよよ is not.
            # `-> Having the same ideograph after a space as the last ideograph before a space is also acceptable. E.g. Grrr r => 貌よ一よ よ
            if isCipherKey("Padding") == False:
                char += 1
                continue
            # ,-> This means Padding=... is part of the *.ini file. Now we just need to check if we should pad the letter with a bonus ideograph.
            if secrets.choice(range(0, FIRST_PADDING_CHANCE)) >= int((FIRST_PADDING_CHANCE / SECOND_PADDING_CHANCE)):
                # `-> These DEFINES are at the top of the code. If you want to modify them or the calculation, feel free.
                ideos = CIPHER_TABLE["Padding"]
                ideos = ideos.replace(lastChar, "", 1)
                current = ideos[secrets.choice(range(0, len(ideos)))]
                output = output + current
                lastChar = current
            char += 1
            continue
        if string[char] == " ":
            # `-> Check to see if Space=... exists in the *.ini file. If it does, do the same as above, otherwise...
            if isCipherKey("Space") == False:
                output = output + " "
                lastChar = ""
            # >-> I simply didn't want to set up a flag to skip this check so I'm checking it twice.
            if isCipherKey("Space") == True:
                ideos = CIPHER_TABLE["Space"]
                ideos = ideos.replace(lastChar, "", 1)
                current = ideos[secrets.choice(range(0, len(ideos)))]
                output = output + current
                lastChar = current
            if isCipherKey("Padding") == False:
                char += 1
                continue
            if secrets.choice(range(0, FIRST_PADDING_CHANCE)) >= int((FIRST_PADDING_CHANCE / SECOND_PADDING_CHANCE)):
                ideos = CIPHER_TABLE["Padding"]
                ideos = ideos.replace(lastChar, "", 1)
                current = ideos[secrets.choice(range(0, len(ideos)))]
                output = output + current
                lastChar = current
            char += 1
            continue
        return
        # ¦-> End here. Having an erroneous character is a flaw.
        # `-> Either type out the word manually (E.g. pounds vs. £ or add the character to the CharOrder in Ideo.ini.)
    return output
    # `-> Return the output.

def main():
    if os.path.exists(IDEO_INI) == False:
        print("Failed to create CIPHER_TABLE! {} is either missing or has been renamed.\n".format(IDEO_INI))
        return
    # ,-> ConfigParser wasn't handling the *.ini file very well - or at all, for that matter - so this is my working solution.
    with open(IDEO_INI, "r", encoding="UTF-8") as thisFile:
        for thisLine in thisFile:
            thisNewLine = thisLine.split("=", 1)
            if len(thisNewLine) < 2:
                continue
            theseChars = re.split(NEWLINE_REGEX, thisNewLine[1])
            if len("".join(theseChars)) > 0:
                # `-> Ignore any entries with zero characters after =. E.g. Extra=
                CIPHER_TABLE[thisNewLine[0]] = "".join(theseChars)

if __name__ == "__main__":
    main()


# EOF
