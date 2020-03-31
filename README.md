                                       ___                            _   
                                      / __\___  _ __ _ __ _   _ _ __ | |_ 
                                     / /  / _ \| '__| '__| | | | '_ \| __|
                                    / /__| (_) | |  | |  | |_| | |_) | |_ 
                                    \____/\___/|_|  |_|   \__,_| .__/ \__|
                                                               |_|        
# Python utilities to corrupt some input text

Script that takes some text as input and randomly modify words by using either
- Levenshtein edit operations
- Synonym replacement, based on an open source Thesaurus from the Libre Office project (as reported in section 2.4 of paper below)

Corruptions can be used as a data augmentation technique, or to benchmark NLP models robustness to misspells and/or synonyms.

Requires: numpy, requests, joblib
## Set up
```bash
$ pip install git+https://github.com/aylliote/corruption.git@master
```
## Exemple
```python
from corruption import Corrupter

corrupter = Corrupter()
sample = "Il fut attiré par cette belle couleur et décida d’y séjourner quelque temps"
corrupter.corrupt(sample, syn=1, typo=0)
>>> 'Il fut prédisposé par une charmante coloriant et décida d’y habiter pour période'

corrupter.corrupt(sample, syn=0, typo=3)
>>> 'Il mfut tatiré par cetet belle colueur et wécida d’y sgjourner quelque temzps'

corrupter.corrupt(sample, syn=2, typo=3)
>>> 'Il fut sujet pax la admirable tilnctorial et décidau d’y habiter auprès âge'
```
## CLI Usage

    usage: corruption [-h] [--col COL] [--seed SEED] [--syn SYN] [--typo TYPO]
                      [--typo-first] [--n_workers N_WORKERS]
                      input output
    
    Corrupt some input text with synonym and mispells.
    
    positional arguments:
      input                 path to input CSV to corrupt
      output                output file to save result CSV
    
    optional arguments:
      -h, --help            show this help message and exit
      --col COL             Column that contains the text to be corrupted
      --seed SEED           Seed for reproducibility (defaults to 2020)
      --syn SYN             Number of synonym corruption iterations (defaults to
                            0)
      --typo TYPO           Number of misspell corruption iterations (defaults to
                            0)
      --typo-first          Inject misspells before synonyms (defaults to False)
      --n_workers N_WORKERS
                            Number of threads for joblib parallelisation, 0 for
                            non-parallelisation (defaults to 0)
## Reference
```bibtex
@misc{zhang2015characterlevel,
    title={Character-level Convolutional Networks for Text Classification},
    author={Xiang Zhang and Junbo Zhao and Yann LeCun},
    year={2015},
    eprint={1509.01626},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```