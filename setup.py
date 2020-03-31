import setuptools


setuptools.setup(
    name='corruption',
    version='0.0.1',
    description='Python utilities to corrupt some input text',
    author='Elliot',
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={ 'console_scripts': ['corruption=corruption.bin.corrupt:main'] })
