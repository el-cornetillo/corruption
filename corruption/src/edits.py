import string
from typing import List, Tuple

letters = string.ascii_lowercase

TRANSPOSE = 'TRANPOSE'
REPLACE = 'REPLACE'
DELETE = 'DELETE'
INSERT = 'INSERT'


def deletes(splits: List[Tuple[str]]) -> List[str]:
    return [left + right[1:] for left, right
            in splits if right]


def tranposes(splits: List[Tuple[str]]) -> List[str]:
    return [left + right[1] + right[0] + right[2:] for left, right
            in splits if len(right) > 1]


def replaces(splits: List[Tuple[str]]) -> List[str]:
    return [left + letter + right[1:] for left, right
            in splits if right for letter in letters]


def inserts(splits: List[Tuple[str]]) -> List[str]:
    return [left + letter + right for left, right
            in splits for letter in letters]
