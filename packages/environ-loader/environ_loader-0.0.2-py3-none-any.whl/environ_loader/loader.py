import os
import copy
from collections import OrderedDict
from typing import MutableMapping, Callable, List, Dict, Generator, Union, KeysView, cast, TYPE_CHECKING
from .var_list import var_list
import contextlib


@contextlib.contextmanager
def scratch_environ(remove : List[str] = [], add : Dict[str,str] = {}) -> Generator[None,None,None]:
    """
    Temporarily modify the ``os.environ`` dictionary.
    """
    env:MutableMapping[str, str] = os.environ.copy()

    try:
        for k in remove:
            del os.environ[k]
        for k in add:
            os.environ[k] = add[k]

        yield
    finally:
        if TYPE_CHECKING:
            EnvironType = os._Environ[str]
        else:
            EnvironType = os._Environ
        os.environ = cast(EnvironType,env)


class dict_with_default_view:
    def __init__(self, store: MutableMapping[str, str], default: str = "") -> None:
        self.store = store
        self.default = default

    def __getitem__(self, k: str) -> str:
        if k in self.store:
            return self.store[k]
        return self.default


def load_vars_into_environment(
    vars: var_list,
    expander: Callable[[str], str] = os.path.expandvars,
    overwrite: bool = True,
) -> None:
    """
    Load variables from 'vars' into dict-like environ (os.environ by default).
    """
    for k, v in vars.items():
        if not overwrite and k in os.environ:
            continue
        os.environ[k] = expander(v)
