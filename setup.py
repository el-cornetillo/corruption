import os.path as osp

import setuptools


setuptools.setup(
    name='corruption',
    version='0.0.2',
    description='Python utilities to corrupt some input text',
    author='Elliot',
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.18.*', 'requests==2.23.*'],
    entry_points={ 'console_scripts': ['corruption=corruption.bin.corrupt:main'] },
    data_files=[('data', [osp.join('corruption', 'data', 'THESAURUS.DAT')])]
)
