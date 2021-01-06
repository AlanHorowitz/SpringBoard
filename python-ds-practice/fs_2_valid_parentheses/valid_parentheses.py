def valid_parentheses(parens):
    """Are the parentheses validly balanced?

        >>> valid_parentheses("()")
        True

        >>> valid_parentheses("()()")
        True

        >>> valid_parentheses("(()())")
        True

        >>> valid_parentheses(")()")
        False

        >>> valid_parentheses("())")
        False

        >>> valid_parentheses("((())")
        False

        >>> valid_parentheses(")()(")
        False
    """
    
    opens = 0
    for ch in parens:
        if ch == '(':
            opens += 1
        elif ch == ')':
            if opens == 0:
                return False
            else:
                opens -= 1
    return opens == 0