# Ideograph Cipher
Ideograph Cipher (<i>formerly</i> Japanese Character Cipher) - Proof of Concept

I'm not really in the habit of rehashing things I've already written elsewhere; so a blog post I wrote <a href="https://jigsy1.blogspot.com/2017/12/my-attempt-at-creating-substitution.html">here</a> [jigsy1.blogspot.com] can explain this.

## Decryption Challenges:

If you want to try decrypting some messages I wrote purely to see if they can be cracked, click these links:

09/02/2023: Sadly, due to circumstances beyond my control - such as the password for the VeraCrypt file these were stored in being apparently incorrect - I've had to completely remake these. I will make a note of the links and re-add them if possible if by some freak of magic I'm able to get back into the file.

12/02/2023: Turns out two of the unused Characters had been part of the main character base for the last six years. Therefore, if you plan on trying to crack these, I recommend adding all of the unused characters to the roster. (Since a computer can tell the difference between the two.)

1. <a href="https://github.com/Jigsy1/IdeoCipher/issues/2">1st implementation</a> - Straightforward. Uses a different character order and key structure than the example, obviously. (EASY MODE)
2. <a href="https://github.com/Jigsy1/IdeoCipher/issues/3">2nd implementation</a> - Spaces encoded. Uses the same character order but key structure is different than the first implementation. (NORMAL MODE)
3. <a href="https://github.com/Jigsy1/IdeoCipher/issues/4">3rd implementation</a> - Spaces encoded and padding characters inserted into the string. Uses the same character order but key structure is different than the other two implementations. (HARD MODE)
4. <a href="https://github.com/Jigsy1/IdeoCipher/issues/5">Extended implementation</a> - Same settings as the third; but uses the extended file (27,622 ideographs). Uses a different character order and key structure than the example implementation. (LUNATIC MODE)

## Ideas:

1. Cyber-Wire sevreal years ago on IRC suggested inserting fake spaces into the string if Space=... is true.
2. Duplicate character checker for the Python version to warn user if same character is elsewhere in the Keys.

## (Possible) Issues:
1. Encoding with Space= enabled, then changing the name to something like Spaces= and trying to decode the message will return something like "This!is!a!test." The same problem also happens with Null= being renamed. This shouldn't be an issue however as long as both parties have the exact same .ini structure.

###### Other Updates:
1. Found a <a href="https://archive.is/NhTlU">very large list</a> [rikai (archived)] of Ideographs (>20,000) and created another example key structure file now located in /extended/. (sqrt on IRC told me that a large majority of them are Chinese ideographs, so the cipher has been renamed.)
