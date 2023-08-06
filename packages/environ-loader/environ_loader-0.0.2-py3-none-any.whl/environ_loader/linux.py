import os
import pathlib
from .var_list import var_list


def get_environ_vars_from_sh_file(file:str) -> var_list:
    """
    Load environment variables from a bash .sh file.
    """
    filepath = pathlib.Path(file)

    vars : var_list = var_list()

    text = filepath.read_text()
    lines = filter( lambda l: l is not None and len(l) > 0 and l.count("=") == 1, map(lambda l: l.strip(), text.strip().split("\n") ) )

    for line in lines:
        k:str
        v:str
        k,v = line.split("=")
        vars.add(k,v)
        


    return vars


def expand_environ_var_value_with_bash(val:str) -> str:
    return "NOT IMPLEMENTED"
