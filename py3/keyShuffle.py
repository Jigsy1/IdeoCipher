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
KEYSHUFFLE_INI = "keyShuffle.ini"
OUTPUT_FILE = "Ideo_{}.ini".format(TIMESTAMP)


# Function(s):

def makeBool(userInput):
    """Convert to either true (1) or false (0)."""
    userInput.lower()
    if userInput == "1" or userInput == "ok" or userInput == "on" or userInput == "t" or userInput == "true" or userInput == "y" or userInput == "yes":
        return 1
    return 0

def main():
    if os.path.exists(IDEO_INI) == False:
        print("Aborting. {} is either missing or has been renamed.\n".format(IDEO_INI))
        return
    START_INDEX = 0
    # `-> If you wish to use the mIRC version, change this to 1. Otherwise, leave it at 0.
    if START_INDEX < 0 or START_INDEX > 1:
        print("Aborting. START_INDEX must be either 0 (Python) or 1 (mIRC).\n")
        return
    SUBTRACT_BY = 0
    LEFTOVER_FLAG = 0
    RANDOMIZE_CHAR_ORDER = 1
    USE_SPACE = 1
    USE_PADDING = 1
    # `-> Defaults; these will be toggled by the code.
    SHUFFLE = []
    UNUSED = ""
    # ,-> ConfigParser wasn't handling the *.ini file very well - or at all, for that matter - so this is my working solution.
    if os.path.exists(KEYSHUFFLE_INI) == True:
        with open(KEYSHUFFLE_INI, "r", encoding="UTF-8") as shuffleFile:
            for keyLine in shuffleFile:
                thisKeyLine = keyLine.split("=", 1)
                if len(thisKeyLine) < 2:
                    continue
                theseSettings = re.split(NEWLINE_REGEX, thisKeyLine[1])
                if thisKeyLine[0] == "RANDOMIZE_CHAR_ORDER":
                    RANDOMIZE_CHAR_ORDER = makeBool(theseSettings[0])
                    continue
                if thisKeyLine[0] == "SUBTRACT_BY_PLUS":
                    SUBTRACT_BY_PLUS = makeBool(theseSettings[0])
                    continue
                if thisKeyLine[0] == "USE_SPACE":
                    USE_SPACE = makeBool(theseSettings[0])
                    continue
                if thisKeyLine[0] == "USE_PADDING":
                    USE_PADDING = makeBool(theseSettings[0])
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
    if RANDOMIZE_CHAR_ORDER == 1:
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
        PLUS_COUNT = 0
        if USE_SPACE == 1:
            PLUS_COUNT += 1
        if USE_PADDING == 1:
            PLUS_COUNT += 1
        KEY_COUNT = len(CHAR_ORDER)
        if SUBTRACT_BY_PLUS == 1:
            SUBTRACT_BY = PLUS_COUNT
        CHARS_PER_LINE = int(((len(SHUFFLE) / len(CHAR_ORDER)) - SUBTRACT_BY))
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
        if PLUS_COUNT > 0:
            DONE_SPACE = 0
            DONE_PADDING = 0
            KEY_COUNT = PLUS_COUNT
            CHARS_PER_LINE = int((len(SHUFFLE) / PLUS_COUNT))
            while KEY_COUNT > 0:
                KEY_LINE = ""
                KEY_SUBCOUNT = 0
                START_LENGTH = len(SHUFFLE)
                while KEY_SUBCOUNT < CHARS_PER_LINE:
                    if START_LENGTH == 0:
                        # `-> Failsafe.
                        break
                    randomIndex = secrets.choice(range(0, len(SHUFFLE)))
                    KEY_LINE = KEY_LINE + SHUFFLE[randomIndex]
                    del SHUFFLE[randomIndex]
                    KEY_SUBCOUNT += 1
                if USE_SPACE == 1 and DONE_SPACE == 0:
                    if len(KEY_LINE) > 0:
                        outputFile.write("{}={}\n".format("Space", KEY_LINE))
                    DONE_SPACE = 1
                    KEY_COUNT -= 1
                    continue
                if USE_PADDING == 1 and DONE_PADDING == 0:
                    if len(KEY_LINE) > 0:
                        outputFile.write("{}={}\n".format("Padding", KEY_LINE))
                    DONE_PADDING = 1
                    KEY_COUNT -= 1
                    continue
                KEY_COUNT -= 1
        if UNUSED != "":
            outputFile.write("Unused={}\n".format(UNUSED))
        if len(SHUFFLE) > 0:
            # ,-> This will be used depending on factors. I can only suggest cutting and pasting them onto the end of 
            # ¦-> certain rows manually...
            outputFile.write("Leftover={}\n".format("".join(SHUFFLE)))
            LEFTOVER_FLAG = 1
    print("Done. Please rename {} to {} before using.\n".format(OUTPUT_FILE, IDEO_INI))
    if LEFTOVER_FLAG == 1:
        print("Warning: Certain characters were leftover due to irregular line division and will not be used unless manually dealt with.\n")

if __name__ == "__main__":
    main()


# EOF
