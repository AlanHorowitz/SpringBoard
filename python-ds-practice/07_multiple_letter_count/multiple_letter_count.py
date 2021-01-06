def multiple_letter_count(phrase):
    """Return dict of {ltr: frequency} from phrase.

        >>> multiple_letter_count('yay')
        {'y': 2, 'a': 1}

        >>> multiple_letter_count('Yay')
        {'Y': 1, 'a': 1, 'y': 1}
    """
    d = {}
    for l in phrase:
        if l in d:
            d[l] = d[l] + 1
        else:
            d[l] = 1
    return d