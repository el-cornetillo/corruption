from typing import List, Tuple, Optional, Union, Callable

import joblib
import numpy as np
import pandas as pd

from .abstract import AbstractCorrupter
from .misspell import MisspellCorrupter
from .synonym import SynonymsCorrupter


class Corrupter:
    _DEFAULT_SEED = 2020


    def __init__(self, prng: Optional[np.random.RandomState] = None):
        self.prng = prng or np.random.RandomState(Corrupter._DEFAULT_SEED)
        self._synonym_corrupter = SynonymsCorrupter(self.prng)
        self._misspell_corrupter = MisspellCorrupter(self.prng)


    @staticmethod
    def _corrupt_wrapper(operations: List[Tuple[AbstractCorrupter, int]]) -> Callable[[str], str]:

        def wrapped(utterance: str):
            for corrupter, iterations in operations:
                utterance = corrupter.corrupt(utterance, iterations)
            return utterance


        return wrapped


    def corrupt(self, obj: Union[pd.DataFrame, str, List[str]], syn: int = 0, typo: int = 0,
                typo_first: bool = False, n_workers: int = 0, col: Optional[str] = None):

        operations = [(self._synonym_corrupter, syn),
                      (self._misspell_corrupter, typo)]
        if typo_first:
            operations.reverse()

        if isinstance(obj, pd.DataFrame):
            if col is None:
                raise ValueError('Input is a DataFrame but no column has been specified. '
                                 'Set a "col" parameter for the column to corrupt')
            if col not in obj.columns:
                raise KeyError(f'"{col}" has not been found in DataFrame')
            obj = obj[col].astype(str).tolist()

        if isinstance(obj, str):
            return Corrupter._corrupt_wrapper(operations)(obj)
        elif isinstance(obj, list):
            wrapped = Corrupter._corrupt_wrapper(operations)
            if n_workers > 0:
                parallel = joblib.Parallel(n_workers, backend="threading", prefer="threads")
                return parallel(joblib.delayed(wrapped(utt) for utt in obj))
            else:
                return [*map(wrapped, obj)]
        else:
            raise ValueError('Input should be a string utterance, a list of string utterances '
                             'or a pd.DataFrame containing utterances to be corrupted')
