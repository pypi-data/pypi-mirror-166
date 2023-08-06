import os

def _str_grep(input_str, search_str, prepend=''):
    out_str = ''
    for l in input_str.split('\n'):
        if search_str in l:
            out_str = out_str + prepend + l.strip() + '\n'

    return out_str.rstrip()

def mgrep(fpath, search_array, prepend='',root='.'):
    """
    Grep strings in file and return matching lines.

    **Parameters:**

    ``fpath``: string
        File path to grep
    ``search_array``: array of strings
        Each element of the array is an string to grep in ``fpath``.
    ``prepend``: string
        prepend string ``prepend`` to each matching line.
    ``root``: string
        File to grep should be in ``root/fpath``.
    """
    abs_path = os.path.join(root,fpath)
    out_str = ''
    if os.path.isfile(abs_path):
        fstr = open(abs_path).read()

        for attr in search_array:
            ostr = _str_grep(fstr,attr,prepend=prepend)

            if ostr != '':
                out_str = out_str + prepend + ostr.strip() + '\n'

    return out_str.rstrip()
