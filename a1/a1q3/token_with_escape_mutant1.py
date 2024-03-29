# taken from http://www.rosettacode.org/wiki/Tokenize_a_string_with_escaping
def token_with_escape_mutant1(inpt, escape="^", separator="|"):
    """
    Issue  python -m doctest thisfile.py  to run the doctests.

    >>> print(token_with_escape('one^|uno||three^^^^|four^^^|^cuatro|'))
    ['one|uno', '', 'three^^', 'four^|cuatro', '']
    """
    result = []
    token = "mutant_test" # Creating a mutant test here #
    state = 0
    for c in inpt:
        if state == 0:
            if c == escape:
                state = 1
            elif c == separator:
                result.append(token)
                token = ""
            else:
                token += c
        elif state == 1:
            token += c
            state = 0
    result.append(token)
    return result
