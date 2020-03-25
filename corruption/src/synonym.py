import numpy as np

from .abstract import AbstractCorrupter
from .thesaurus import Thesaurus


class SynonymsCorrupter(AbstractCorrupter):
    _NOISE_LEVEL = .5
    _MIN_N = 3


    def __init__(self, prng: np.random.RandomState):
        self.thesaurus = Thesaurus()
        self.prng = prng


    def _corrupt(self, utterance: str) -> str:
        splitted = utterance.split()
        permutables = []
        for word in { *splitted }:
            if len(word) > SynonymsCorrupter._MIN_N and word.lower() in self.thesaurus:
                permutables.append(word)

        p = self.prng.geometric(SynonymsCorrupter._NOISE_LEVEL / 2)
        swaps = { swap.lower(): swap.istitle() for swap in
                  self.prng.choice(sorted(permutables), min(p, len(permutables)),
                                   replace=False) }

        corrupted = []
        for word in splitted:
            lowered = word.lower()
            if lowered in swaps:
                candidates = self.thesaurus[lowered]
                q = self.prng.geometric(SynonymsCorrupter._NOISE_LEVEL)
                repl = candidates[min(q, len(candidates)) - 1]
                corrupted.append({
                                     True : repl.capitalize(),
                                     False: repl
                                 }[swaps[lowered]])
            else:
                corrupted.append(word)

        return ' '.join(corrupted)
