def vowel_count(phrase):
    """Return frequency map of vowels, case-insensitive.

        >>> vowel_count('rithm school')
        {'i': 1, 'o': 2}
        
        >>> vowel_count('HOW ARE YOU? i am great!') 
        {'o': 2, 'a': 3, 'e': 2, 'u': 1, 'i': 1}
    """
    # Add a comment to practice committing from VS Code
    low_phrase = phrase.lower()
    d = {}
    for l in low_phrase:
        if l in "aeiou":
            if l in d:
                d[l] = d[l] + 1
            else:
                d[l] = 1
    return d
        