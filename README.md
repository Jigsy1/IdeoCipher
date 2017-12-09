# JCC
Japanese Character Cipher - Proof of Concept

Not in the habit of rehashing things I've already written, so a blog post I wrote <a href="https://jigsy1.blogspot.com/2017/12/my-attempt-at-creating-substitution.html">here</a> [jigsy1.blogspot.com] can explain this.

<h1>Decryption Challenges:</h1>

If you want to try decrypting some messages I wrote purley to see if they can be cracked:

1. <a href="https://pastebin.com/raw/frQ7SMZ3">1st implementation</a> [pastebin] - Uses a different key structure
2. <a href="https://pastebin.com/raw/QwN9NQrg">2nd implementation</a> [pastebin] - Encoded spaces, different key structure than the 1st.
3. <a href="https://pastebin.com/raw/6A6rs43Y">3rd implementation</a> [pastebin] - Encoded spaces, null characters and a different key structure than the other two.

<h1>Ideas:</h1>

1. <s>Wondering if spaces should also be encrypted.</s>
2. Wondering if invalid characters should use the "similar looking" characters. (ロ & 口, ニ & 二, etc.)
3. <s>Maybe a way of using similar looking characters as long as there's a way of checking the duplicates twice (E.g. ロ wasn't found, so it's probably the other one). The only problem with this is if someone writes down the ciphertext.</s>
4. <a>Null=[chars] - Basically characters that represent no value, but randomly added to a message purely to slow down decryption attacks. (Would be ignored during decoding.)</a>

<h1>Progress:</h1>

1. Added. Basically it checks to see if Space=... is in the .ini.
2.
3. This didn't seem to be an issue in mIRC. It could seem to tell the difference between へ (Hiragana) and ヘ (Katakana). The only issue that arises with this is, again, if somebody writes the message down onto a piece of paper. Also the characters shouldn't be used for the same character, because of the whole doppelgänger problem.
4. Added, but currently testing for the time being.
