# keyShuffle.py (Experimental) by Jigsy (https://github.com/Jigsy1) released under the Unlicense.
#
# For shuffling the (default) Ideo.ini keys automatically rather than doing it manually.

import os
import re
import secrets
import time


# define(s):

NEWLINE_REGEX = r"[\n\r]+"
# `-> For splitting on main().

TIMESTAMP = str(time.time())

IDEO_INI = "Ideo.ini"
OUTPUT_FILE = "Ideo_{}.ini".format(TIMESTAMP)

RANDOMIZE_CHARS = 1
# `-> Randomize the CharOrder. 1 = Yes; 0 = No.


# Function(s):

def main():
    if os.path.exists(IDEO_INI) == False:
        print("Aborting. {} is either missing or has been renamed.\n".format(IDEO_INI))
        return
    START_INDEX = 0
    # `-> If you wish to use the mIRC version, change this to 1. Otherwise, leave it at 0.
    if START_INDEX < 0 or START_INDEX > 1:
        print("Aborting. START_INDEX must be either 0 (Python) or 1 (mIRC).\n")
        return
    SHUFFLE = []
    UNUSED = ""
    # ,-> ConfigParser wasn't handling the *.ini file very well - or at all, for that matter - so this is my working solution.
    with open(IDEO_INI, "r", encoding="UTF-8") as thisFile:
        for thisLine in thisFile:
            thisNewLine = thisLine.split("=", 1)
            if len(thisNewLine) < 2:
                continue
            theseChars = re.split(NEWLINE_REGEX, thisNewLine[1])
            if len("".join(theseChars)) > 0:
                # `-> Ignore any entries with zero characters after the =. E.g. Extra=
                if thisNewLine[0] == "CharOrder":
                    CHAR_ORDER = "".join(theseChars)
                    continue
                if thisNewLine[0] == "Unused":
                    UNUSED = "".join(theseChars)
                    continue
                chars = "".join(theseChars)
                char = 0
                while char < len(chars):
                    SHUFFLE.append(chars[char])
                    char += 1
    if RANDOMIZE_CHARS == 1:
        PRE_ORDER = list(CHAR_ORDER)
        NEW_ORDER = []
        ORDER_COUNT = len(PRE_ORDER)
        while ORDER_COUNT > 0:
            randomChar = secrets.choice(range(0, len(PRE_ORDER)))
            NEW_ORDER.append(PRE_ORDER[randomChar])
            del PRE_ORDER[randomChar]
            ORDER_COUNT -= 1
        CHAR_ORDER = ""
        CHAR_ORDER = "".join(NEW_ORDER)
        del PRE_ORDER
        del NEW_ORDER
    # ,-> Shuffle the list randomly at least once.
    KEY_COUNT = len(SHUFFLE)
    PRE_SHUFFLE = []
    while KEY_COUNT > 0:
        randomIndex = secrets.choice(range(0, len(SHUFFLE)))
        PRE_SHUFFLE.append(SHUFFLE[randomIndex])
        del SHUFFLE[randomIndex]
        KEY_COUNT -= 1
    SHUFFLE.clear()
    SHUFFLE = PRE_SHUFFLE.copy()
    del PRE_SHUFFLE
    # ,-> Second shuffle, but write them out this time.
    with open(OUTPUT_FILE, "w", encoding="UTF-8") as outputFile:
        outputFile.write("# File generated at: {}\n".format(TIMESTAMP))
        if START_INDEX == 1:
            outputFile.write("#\n")
            outputFile.write("# This is only compatible with the mIRC version of ideoCipher.\n")
        outputFile.write("\n")
        outputFile.write("[Settings]\n")
        outputFile.write("CharOrder={}\n\n".format(CHAR_ORDER))
        outputFile.write("[Keys]\n")
        KEY_COUNT = len(CHAR_ORDER)
        CHARS_PER_LINE = int((len(SHUFFLE) / len(CHAR_ORDER)))
        # CHARS_PER_LINE = int(((len(SHUFFLE) / len(CHAR_ORDER)) - 1))
        # `-> Subtract one line because we need to split between Space and Padding on the last line. (Results in longer Space and Padding.)
        while KEY_COUNT > 0:
            KEY_LINE = ""
            KEY_SUBCOUNT = 0
            while KEY_SUBCOUNT < CHARS_PER_LINE:
                randomIndex = secrets.choice(range(0, len(SHUFFLE)))
                KEY_LINE = KEY_LINE + SHUFFLE[randomIndex]
                del SHUFFLE[randomIndex]
                KEY_SUBCOUNT += 1
            outputFile.write("{}={}\n".format(START_INDEX, KEY_LINE))
            START_INDEX += 1
            KEY_COUNT -= 1
        KEY_COUNT = 2
        CHARS_PER_LINE = int((len(SHUFFLE) / 2))
        while KEY_COUNT > 0:
            KEY_LINE = ""
            KEY_SUBCOUNT = 0
            while KEY_SUBCOUNT < CHARS_PER_LINE:
                randomIndex = secrets.choice(range(0, len(SHUFFLE)))
                KEY_LINE = KEY_LINE + SHUFFLE[randomIndex]
                del SHUFFLE[randomIndex]
                KEY_SUBCOUNT += 1
            if KEY_COUNT == 2:
                outputFile.write("{}={}\n".format("Space", KEY_LINE))
            else:
                outputFile.write("{}={}\n".format("Padding", KEY_LINE))
            KEY_COUNT -= 1
        if UNUSED != "":
            outputFile.write("Unused={}\n".format(UNUSED))
        if len(SHUFFLE) > 0:
            # `-> Hopefully this won't be used. If it is, just cut and paste them into either Space or Padding manually I guess?
            outputFile.write("Leftover={}\n".format("".join(SHUFFLE)))
    print("Done. Please rename {} to {} before using.\n".format(OUTPUT_FILE, IDEO_INI))

if __name__ == "__main__":
    main()


# EOF
