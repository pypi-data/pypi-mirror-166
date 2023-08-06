from ctypes import CDLL
from ctypes.util import find_library


def load():
    LIBNAME = "ApplicationServices"

    if libpath := find_library(LIBNAME):
        return CDLL(libpath)

    raise OSError(f"Library {LIBNAME} not found.")
