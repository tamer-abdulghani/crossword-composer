WORD_LIST = [w.strip() for w in open("words.txt", "r").readlines()]


def search_words(letters):
    """ Search for a word by using letter constraints.
    Provide a list of letters (in caps), and an empty string for any letter.

    For example: search_words(["H","","L","L",""])
    ['HALLO',
    'HALLS',
    'HELLO',
    'HELLS',
    'HILLO',
    'HILLS',
    'HILLY',
    'HOLLA',
    'HOLLO',
    'HOLLY',
    'HULLO',
    'HULLS',
    'HULLY']
    """
    valid_words = []
    for w in WORD_LIST:
        if len(w) == len(letters):
            valid = True
            for i in range(len(letters)):
                if ((letters[i] != "") and (letters[i] != w[i])):
                    valid = False
            if valid:
                valid_words += [w]

    return valid_words


def is_word(letters):
    """ Determine whether or not a list of letters (in caps)
    corresponds to a word in the dictionary.
    example:
    >>> utils.is_word(["H", "E", "L", "L", "O"])
    True
    >>> utils.is_word(["H", "E", "L", "L", "P"])
    False
    """
    return "".join(letters) in WORD_LIST
