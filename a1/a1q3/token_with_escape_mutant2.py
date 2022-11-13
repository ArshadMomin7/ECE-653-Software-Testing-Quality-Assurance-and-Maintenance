# taken from http://www.rosettacode.org/wiki/Tokenize_a_string_with_escaping
def token_with_escape_mutant2(inpt, escape="^", separator="|"):
    """
    Issue  python -m doctest thisfile.py  to run the doctests.

    >>> print(token_with_escape('one^|uno||three^^^^|four^^^|^cuatro|'))
    ['one|uno', '', 'three^^', 'four^|cuatro', '']
    """
    result = []
    token = ""
    state = 1 # Changed value of state from 0 to 1
    for c in inpt:
        if state == 0: 
            if c == separator: #Creating another mutation here by changing value of c== escape to c== separator
                state = 0 # Changed value of state from 1 to 0
            elif c == escape: #Creating another mutation here by changing value of c== separator to c== escape
                result.append(token)
                token = ""
            else:
               token += c
        elif state == 1:
         token += c
         state = 0
    result.append(token)
    return result
