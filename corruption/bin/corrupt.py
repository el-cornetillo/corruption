import argparse
import sys

import numpy as np


if __name__ == "__main__" and eval('__package__') is None:
    __package__ = "corruption.bin"

from ..src import MisspellCorrupter, SynonymsCorrupter


def parse_args(args):
    parser = argparse.ArgumentParser(description='Corrupt some input text with synonym and mispells.')

    parser.add_argument('utterance',
                        help='Utterance to corrupt')
    parser.add_argument('--seed',
                        help='Seed', default=2020, type=int)
    parser.add_argument('--syn',
                        help='Number of synonym corruption iterations', default=0, type=int)
    parser.add_argument('--typo',
                        help='Number of misspell corruption iterations', default=0, type=int)

    parser.add_argument('--typo-first',
                        help="Inject misspells before synonyms", action='store_true')

    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parse_args(args)
    prng = np.random.RandomState(seed=args.seed)

    utterance = args.utterance

    synonym_corrupter = SynonymsCorrupter(prng=prng)
    misspell_corrupter = MisspellCorrupter(prng=prng)

    operations = [*zip([synonym_corrupter, misspell_corrupter], [args.syn, args.typo])]

    if args.typo_first:
        operations.reverse()

    for corrupter, iterations in operations:
        utterance = corrupter.corrupt(utterance, iterations)

    print('*' * 30)
    print(utterance)
    print('*' * 30)


if __name__ == '__main__':
    main()
