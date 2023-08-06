import os

def _str_grep(input_str, search_str, prepend=''):
    out_str = ''
    for l in input_str.split('\n'):
        if search_str in l:
            out_str = out_str + prepend + l.strip() + '\n'

    return out_str.rstrip()

def mgrep(filepath: str, search_array: list[str], prepend:str ='',root:str ='.') -> str:
    """Grep strings in file and return matching lines.

    Parameters
    ----------
    filepath
        File path to grep
    search_array
        Each element of the array is an string to grep in ``filepath``.
    prepend
        prepend string ``prepend`` to each matching line.
    root
        File to grep should be in ``root/filepath``.

    Returns
    -------
    str
        Full lines in file matching any of the strings in the `search_array` list
    """
    abs_path = os.path.join(root,filepath)
    out_str = ''
    if os.path.isfile(abs_path):
        fstr = open(abs_path).read()

        for attr in search_array:
            ostr = _str_grep(fstr,attr,prepend=prepend)

            if ostr != '':
                out_str = out_str + prepend + ostr.strip() + '\n'

    return out_str.rstrip()


def replace_line(filepath: str, matching: str, replace_by: str, destpath: str = '', prefix:str = '', suffix:str = '') -> None:
    """Replace all lines of a file matching a string by another string.
    
    If overwrites original file, except in the following two cases:

        - `prefix`, or `suffix` are given,
    
        - `destpath` is given and is different from `os.path.dirname(filepath)`.

    Parameters
    ----------
    filepath
        Path to the file to be edited.
    matching
        Lines containing the string passed to this argument will be replaced.
    replace_by
        Matching lines will be replaced by the string given in this argument.
    prefix
       prefix added to output file name
    suffix
       suffix added to output file name
        
    Returns
    -------
    None
    """
    linestr = mgrep(filepath, [matching])

    # Read in the file
    with open(filepath, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(linestr, replace_by)

    # Write the file out again
    _filepath, _ext = os.path.splitext(filepath)

    if destpath == '':
        newpath = os.path.dirname(_filepath) + prefix + os.path.basename(_filepath) + suffix + _ext
    else:
        newpath = os.path.join(destpath, prefix + os.path.basename(_filepath) + suffix + _ext)        
        
    with open(newpath, 'w') as file:
        file.write(filedata)

def dummy():
    pass
