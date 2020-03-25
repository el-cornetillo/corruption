import json
import os
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

import requests

osp = os.path


class Thesaurus:
    _ZIPURL = "https://grammalecte.net/download/fr/thesaurus-v2.3.zip"
    _THESAURUS_PATH = 'THESAURUS.DAT'
    _DATFILE = 'thes_fr.dat'
    _SEP = '|'


    def __init__(self):
        datapath = Thesaurus._fetch_thesaurus(Thesaurus._THESAURUS_PATH)
        self._data = json.load(open(datapath, 'r', encoding='utf8'))


    def __getitem__(self, key: str):
        return self._data.get(key, [])


    def __len__(self) -> int:
        return len(self._data)


    def __contains__(self, key: str) -> bool:
        return key in self._data


    @staticmethod
    def _fetch_thesaurus(data_path: str) -> str:
        dir_path = osp.join(osp.dirname(__file__), '..')
        data_path = osp.join(dir_path, data_path)
        if not os.path.exists(data_path):
            print('Downloading thesaurus data ...')
            zipfile = ZipFile(BytesIO(requests.get(Thesaurus._ZIPURL).content))
            stream = zipfile.open(Thesaurus._DATFILE)
            encoding = stream.readline().strip().decode()
            words, synonyms = [], []
            for line in stream.read().splitlines():
                line = line.decode(encoding)
                if line.startswith('('):
                    synonyms.append(line.split(Thesaurus._SEP)[1:])
                else:
                    words.append(line)

            export = defaultdict(list)
            counter = 0
            for word in words:
                _repr, _n = word.split(Thesaurus._SEP)
                for offset in range(int(_n)):
                    export[_repr] += synonyms[offset + counter]
                    counter += 1

            os.makedirs(dir_path, exist_ok=True)
            json.dump(dict(export), open(data_path, 'w', encoding=encoding),
                      ensure_ascii=False, sort_keys=True, indent=4)

            print('Thesaurus if fetched')

        return data_path
