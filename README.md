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


## Set up

`pip install git+https://github.com/aylliote/corruption.git@master

## Usage

    usage: corruption [-h] [--seed SEED] [--syn SYN] [--typo TYPO] [--typo-first]
                      utterance

    Corrupt some input text with synonym and mispells.

    positional arguments:
      utterance     Utterance to corrupt

    optional arguments:
      -h, --help    show this help message and exit
      --seed SEED   Seed
      --syn SYN     Number of synonym corruption iterations
      --typo TYPO   Number of misspell corruption iterations
      --typo-first  Inject misspells before synonyms
          
          
 ## Reference
 
     Xiang Zhang and Junbo Zhao and Yann LeCun
     https://arxiv.org/abs/1509.01626
     Character-level Convolutional Networks for Text Classification
     2015
