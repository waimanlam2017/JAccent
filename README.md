# JAccent
Japanese Text Accent Checker

The software was created to analysis the accent of each Japanese word within a text file. It was named JAccent in which the letter J implies Japanese.


Requirement / Dependecies for JAccent:
 - Python 3.5.2 or above
   ( https://www.python.org/ )
 - MeCab: Yet Another Part-of-Speech and Morphological Analyzer
   ( http://taku910.github.io/mecab/ ) 
 - fake-useragent 0.1.10 
   (https://pypi.org/project/fake-useragent/)

Platform:
 - Tested Windows 7 64-bit
 - Tested Ubuntu 16.04 LTS 64-bit

Additional Tips regarding installation of MeCab:
  If you choose to build MeCab from source under linux distribution. It is very important to build/install MeCab and its bundled dictionary in utf-8 encoding, otherwise it would default installed under euc-jp encoding. euc-jp encoding does not work with Python 3.
  There is no such problem in Windows binary released in MeCabs' official website. 
