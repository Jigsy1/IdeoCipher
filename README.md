# JCC
Japanese Character Cipher - Proof of Concept

Not in the habit of rehashing things I've already written, so a blog post I wrote <a href="https://jigsy1.blogspot.com/2017/12/my-attempt-at-creating-substitution.html">here</a> [jigsy1.blogspot.com] can explain this.

If you want to try decrypting a message I wrote - which uses a completely different key structure than the example .ini file - go <a href="https://pastebin.com/raw/frQ7SMZ3">here</a>. [pastebin]

<h1>Ideas:</h1>

1. Wondering if spaces should also be encrypted.
2. Wondering if invalid characters should use the "similar looking" characters. (ロ & 口, ニ & 二, etc.)
3. Maybe a way of using similar looking characters as long as there's a way of checking the duplicates twice (E.g. ロ wasn't found, so it's probably the other one). The only problem with this is if someone writes down the ciphertext.
