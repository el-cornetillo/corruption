from typing import List

import numpy as np

from .abstract import AbstractCorrupter
from .edits import deletes, tranposes, replaces, inserts

__all__ = ['MisspellCorrupter']

TRANSPOSE = 'TRANPOSE'
REPLACE = 'REPLACE'
DELETE = 'DELETE'
INSERT = 'INSERT'


class MisspellCorrupter(AbstractCorrupter):
    _NOISE_LEVEL = .75
    _EDIT_MAP = {
        TRANSPOSE: tranposes,
        REPLACE  : replaces,
        DELETE   : deletes,
        INSERT   : inserts,
    }


    def __init__(self, prng: np.random.RandomState):
        self.prng = prng


    def _corrupt(self, utterance: str) -> str:
        splitted = utterance.split()
        permutables = { *filter(lambda w: w.isalpha(), splitted) }

        p = self.prng.geometric(MisspellCorrupter._NOISE_LEVEL)
        swaps = { swap.lower(): swap.istitle() for swap in
                  self.prng.choice(sorted(permutables), min(p, len(permutables)),
                                   replace=False) }

        corrupted = []
        for word in splitted:
            lowered = word.lower()
            if lowered in swaps:
                candidates = self._random_edits(lowered)
                repl = self.prng.choice(candidates)
                corrupted.append({
                                     True : repl.capitalize(),
                                     False: repl
                                 }[swaps[lowered]])
            else:
                corrupted.append(word)

        return ' '.join(corrupted)


    def _random_edits(self, word: str) -> List[str]:
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        operations = [*MisspellCorrupter._EDIT_MAP]
        if len(word) <= 3:
            operations.remove(DELETE)
        if len(word) <= 2:
            operations.remove(TRANSPOSE)

        mode = self.prng.choice(operations)
        return MisspellCorrupter._EDIT_MAP[mode](splits)
