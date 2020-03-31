import argparse
import os
import sys

import numpy as np
import pandas as pd

from ..src import Corrupter

if __name__ == "__main__" and eval('__package__') is None:
    __package__ = "corruption.bin"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Corrupt some input text with synonym and mispells.')

    parser.add_argument('input',
                        help='path to input CSV to corrupt',
                        type=str)

    parser.add_argument('output',
                        help='output file to save result CSV',
                        type=str)

    parser.add_argument('--col',
                        help='Column that contains the text to be corrupted')

    parser.add_argument('--seed',
                        help='Seed for reproducibility (defaults to 2020)', default=2020, type=int)
    parser.add_argument('--syn',
                        help='Number of synonym corruption iterations (defaults to 0)', default=0, type=int)
    parser.add_argument('--typo',
                        help='Number of misspell corruption iterations (defaults to 0)', default=0, type=int)

    parser.add_argument('--typo-first',
                        help="Inject misspells before synonyms (defaults to False)", action='store_true')

    parser.add_argument('--n_workers',
                        help="Number of threads for joblib parallelisation, 0 for non-parallelisation (defaults to 0)",
                        default=0, type=int)

    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(args)
    obj = args.input

    prng = np.random.RandomState(seed=args.seed)
    corrupter = Corrupter(prng=prng)

    if os.path.exists(obj) and obj.lower().endswith('csv'):
        if args.col is None:
            parser.error("CSV input requires --col")
        df = pd.read_csv(obj)
        df[args.col] = corrupter.corrupt(obj=df, syn=args.syn, typo=args.typo,
                                         typo_first=args.typo_first, n_workers=args.n_workers,
                                         col=args.col)
        df.to_csv(args.output, index=False, encoding='utf8')
    else:
        raise ValueError('Input file does not exist or is not a CSV '
                         f'[received {args.input}]')


if __name__ == '__main__':
    main()
