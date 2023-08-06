
import sys


def clear(dest=""):
    if(len(dest) > 0):
        if dest in sys.path:
            sys.path.remove(dest)
    else:
        if ".." in sys.path:
            sys.path.remove("..")
        if "../.." in sys.path:
            sys.path.remove("../..")
        if "../../.." in sys.path:
            sys.path.remove("../../..")
