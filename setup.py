import os,glob
from setuptools import  setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

datadir = os.path.join('mfiles','wtc')
datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]


setup(
    name = "pybootstrap",
    version = "0.0.1",
    author = "Eduardo dos Santos Pereira",
    author_email = "pereira.somoza@gmail.com",
    description = ("Tools For Bootstrap and Fisher Information Analises in Python"),
    license = "GNU v3",
    keywords = "statistics, bootstrap, Fisher Matrix",
    url = "https://github.com/duducosmos/pybootstrap",
    packages= find_packages(), 
    package_data={'': ['*.txt', '*.html', '*.png']}, 
    data_files= datafiles,
    install_requires=['numpy', 'scipy', 'matplotlib'], 
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GNU V3",
    ],
)
