def same_frequency(num1, num2):
    """Do these nums have same frequencies of digits?
    
        >>> same_frequency(551122, 221515)
        True
        
        >>> same_frequency(321142, 3212215)
        False
        
        >>> same_frequency(1212, 2211)
        True
    """
    freq_1 = [0] * 10
    freq_2 = [0] * 10
    for n in str(num1):
        i = int(n)
        freq_1[i] = freq_1[i] + 1
    for n in str(num2):
        i = int(n)
        freq_2[i] = freq_2[i] + 1
    return freq_1 == freq_2