import getopt
import glob
import os
import os.path
import sys
import wiki_extractor
from tqdm import tqdm
from whoosh import index, qparser, scoring
from whoosh.analysis import *
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from xml.dom import minidom
from indexer import Indexer, Section, Document, Searcher
inputQuery=""
while inputQuery != "exit":
    inputQuery = input("Type your request, otherwise tape 'exit' to exit\n")
    result= Searcher.search(os.getcwd()+"/index",inputQuery)
    if result.is_empty() is True:
        print("No result found")
    else:
        print(result[0]) 