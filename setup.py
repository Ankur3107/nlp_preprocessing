#!/usr/bin/env python

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='nlp_preprocessing',  
     version='0.1.2',
     author="Ankur Singh",
     author_email="ankur310794@gmail.com",
     description="A Package for text preprocessing",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Ankur3107/nlp_preprocessing",
     packages=['nlp_preprocessing'],
     install_requires=['scikit-learn','gensim','numpy'], 
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ]
 )