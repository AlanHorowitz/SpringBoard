def single_letter_count(word, letter):
    """How many times does letter appear in word (case-insensitively)?
    
        >>> single_letter_count('Hello World', 'h')
        1
        
        >>> single_letter_count('Hello World', 'z')
        0
        
        >>> single_letter_count("Hello World", 'l')
        3
    """
    s = 0
    low_letter, low_word = letter.lower(), word.lower()
    for l in low_word:
        if l == low_letter:
            s += 1
    return s
            