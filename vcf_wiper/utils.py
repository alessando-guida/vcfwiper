def remove_commas_from_quoted_strings(string: str, sep: str):
    """ Some lines might have comes or other separators between quotes. Characters
    between quotes should be treated as part of the string and not as separators
    having them there can interfere with the splitting and operations

    Examples
        '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">',

    the comma in the description causes problem. This function converts it into

        '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership build 129">',
    """
    quotes = False
    out = ''

    for char in string:
        if char == '"':
            if quotes:  # exiting quote
                quotes = False
            else:       # entering quote
                quotes = True

        if char == sep and quotes:
            continue

        out += char

    return out


def can_be_float(value) -> bool:
    """check if value is true or not"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def can_be_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def can_be_chr(value) -> bool:
    try:
        str(value)
        if len(str(value)) == 1:
            return True
        else:
            return False
    except:
        return False


def can_be_str(value) -> bool:
    try:
        str(value)
        if value != "":
            return True
        else:
            return False
    except ValueError:
        return False


def can_be_bool(value) -> bool:
    try:
        bool(value)
        if value == 1 or value == 0 or value == False or value == True or value == "False" or value == "True" or \
            value == "1" or value == "0":
            return True
        else:
            return False
    except ValueError:
        return False
