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

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

class DiacriticFilter(PythonTokenFilter):
    def __init__(self, input):
        super().__init__(input)
        self.termAtt = self.addAttribute(CharTermAttribute.class_)
        self.input = input

    def incrementToken(self):
        if self.input.incrementToken():
            text = self.termAtt.toString()
            text = unidecode.unidecode(text)  # This removes accents.
            self.termAtt.setEmpty()
            self.termAtt.append(text)
            return True
        else:
            return False


class MyPythonEnglishAnalyzer(PythonEnglishAnalyzer):
    ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(CharArraySet(Arrays.asList(
        ["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not",
         "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was",
         "will", "with"]), False))

    def __init__(self, stopwords=ENGLISH_STOP_WORDS_SET, stemExclusionSet=CharArraySet.EMPTY_SET):
        super().__init__(self, stopwords)
        self.stopwords = stopwords
        self.stemExclusionSet = stemExclusionSet

    def createComponents(self, fieldName):
        source = StandardTokenizer()
        result = EnglishPossessiveFilter(source)
        result = LowerCaseFilter(result)
        result = DiacriticFilter(result)
        result = StopFilter(result, self.stopwords)
        if self.stemExclusionSet.isEmpty() is False:
            result = SetKeywordMarkerFilter(result, self.stemExclusionSet)
        result = PorterStemFilter(result)
        return Analyzer.TokenStreamComponents(source, result)

    def normalize(self, fieldName, input):
        return LowerCaseFilter(input)
