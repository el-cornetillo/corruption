from abc import ABC, abstractmethod

import numpy as np


class AbstractCorrupter(ABC):
    prng: np.random.RandomState


    @abstractmethod
    def _corrupt(self, utterance: str) -> str:
        raise NotImplementedError


    def corrupt(self, utterance: str, n_iter: int = 1) -> str:
        for _ in range(n_iter):
            utterance = self._corrupt(utterance)
        return utterance
