from src.TreeBuilder import TreeBuilder
from src import TreeBuilder as TB
from src import TrieTree as TT
import pickle

import sys

sys.modules['TrieTree'] = TT
sys.modules['TreeBuilder'] = TB


def load_tree(file: str) -> TreeBuilder:
    """
    Load a tree from file (using pickle)

    :param file: a path to file (string format)
    :return: a TreeBuilder object
    """
    return pickle.load(open(file, "rb"))
