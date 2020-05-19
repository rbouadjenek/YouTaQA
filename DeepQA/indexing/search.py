import getopt
import glob
import os
import os.path
import sys
import lucene
import unidecode
import wiki_extractor
from java.nio.file import Paths
from java.util import Arrays
from org.apache.lucene.analysis import CharArraySet
from org.apache.lucene.analysis import LowerCaseFilter, Analyzer
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.codecs.simpletext import SimpleTextCodec
from org.apache.lucene.document import Document, StringField, Field, TextField
from org.apache.lucene.index import IndexWriterConfig, IndexWriter, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser, QueryParserBase
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import *
from org.apache.lucene.store import FSDirectory
from org.apache.pylucene.analysis import PythonEnglishAnalyzer, PythonTokenFilter
from org.apache.lucene.analysis.en import EnglishPossessiveFilter, PorterStemFilter
from org.apache.lucene.analysis import StopFilter
from org.apache.lucene.analysis.miscellaneous import SetKeywordMarkerFilter
from my_custom_analyzer import *
from indexer import *
from wiki_doc import *
from tqdm import tqdm
from xml.dom import minidom

class Searcher:

    #sim = BM25Similarity()  # or ClassicSimilarity

    def simpleSearch(self, searchDir, query, sim):
        """
        Method that searches through documents using only content_section Field
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        self.analyzer = MyPythonEnglishAnalyzer(stopwords=Indexer.ENGLISH_STOP_WORDS_SET)
        self.directory = FSDirectory.open(Paths.get(searchDir))
        self.reader = DirectoryReader.open(self.directory)
        self.searcher = IndexSearcher(self.reader)
        # Parse a simple query that searches for "text":
        parser = QueryParser("content_section", self.analyzer)
        query = parser.parse(QueryParser.escape(query))
        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(query, 1000).scoreDocs
        return hits

    def MultiFieldsSearch(self, searchDir, query, sim):
        """
        Method that searches through documents using content_section and title_article Fields
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        self.analyzer = MyPythonEnglishAnalyzer(stopwords=Indexer.ENGLISH_STOP_WORDS_SET)
        self.directory = FSDirectory.open(Paths.get(searchDir))
        self.reader = DirectoryReader.open(self.directory)
        self.searcher = IndexSearcher(self.reader)
        parser = MultiFieldQueryParser(
            ["content_section", "title_article"], self.analyzer)
        parser.setDefaultOperator(QueryParserBase.OR_OPERATOR)
        query = MultiFieldQueryParser.parse(parser, QueryParser.escape(query))
        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(query, 1000).scoreDocs
        return hits
