import getopt
import glob
import os
import os.path
import sys
import wiki_extractor
from tqdm import tqdm
import lucene
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriterConfig, IndexWriter, DirectoryReader
from org.apache.lucene.codecs.simpletext import SimpleTextCodec
from org.apache.lucene.store import FSDirectory
from java.nio.file import Path, Paths
from org.apache.lucene.document import Document, StringField, Field, TextField
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis import StopwordAnalyzerBase, CharArraySet
from java.util import List, Arrays
from xml.dom import minidom
from indexer import Indexer, Section, Document, Searcher
from similarity import Similarity
inputQuery = ""
Similarity = Similarity()


while inputQuery != "exit":
    inputQuery = input("Enter your request, otherwise tape 'exit' to exit\n")
    if inputQuery == "exit":
        break
    searchObject = Searcher()
    result = searchObject.MultiFieldsSearch(
        "/Users/younesagabi/Desktop/DeepQA/index_Wiki_v6.0", inputQuery)

    print("#" * 100)
    print("#" * 100)
    content = ""
    for i in range(len(result)):
        hitDoc = searchObject.searcher.doc(result[i].doc)
        content = hitDoc.get("content_section")
        if content != "":
            break
    searchObject.reader.close()
    searchObject.directory.close()
    print(content)
    print("#" * 50)
    CosSim = Similarity.cosine_similarity(inputQuery, content)
    jacSim = Similarity.jaccard_similarity(inputQuery, content)
    diceSim = Similarity.dice_similarity(inputQuery, content)
    print("=> Cosiane similarity : ", CosSim)
    print("=> Jaccard similarity : ", jacSim)
    print("=> Dice similarity : ", diceSim)
    print("#" * 50)
