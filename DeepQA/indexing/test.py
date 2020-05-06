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
from similarity import Similarity
inputQuery = ""
Similarity = Similarity()

while inputQuery != "exit":
    inputQuery = input("Enter your request, otherwise tape 'exit' to exit\n")
    if inputQuery == "exit":
        break
    result = Searcher().search(
        "/Users/younesagabi/Desktop/DeepQA/DeepQA/indexing/index", inputQuery)

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
        print("#" * 100)
        CosSim = Similarity.cosine_similarity(inputQuery, content)
        jacSim = Similarity.jaccard_similarity(inputQuery, content)
        diceSim = Similarity.dice_similarity(inputQuery, content)
        print("=> Cosiane similarity : ", CosSim)
        print("=> Jaccard similarity : ", jacSim)
        print("=> Dice similarity : ", diceSim)
        print("#" * 100)
