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
from cosine_similarity import CosineSimilarity
inputQuery = ""
CosineSimilarity = CosineSimilarity()

while inputQuery != "exit":
    inputQuery = input("Enter your request, otherwise tape 'exit' to exit\n")
    if inputQuery == "exit":
        break
    result = Searcher().search(os.getcwd() + "/index", inputQuery)
    if result.is_empty() is True:
        print("No result found")
    else:
        print("#" * 100)
        print("#" * 100)
        content = ""
        for hit in result:
            content = hit["content_section"]
            if content != "":
                break
        print(content)
        print("#" * 50)
        CosSim = CosineSimilarity.similarity(inputQuery, content)
        print(CosSim)
        print("#" * 100)
