import getopt
import glob
import os
import os.path
import sys
from xml.dom import minidom
from tqdm import tqdm
import lucene
import unidecode
import wiki_extractor
from java.nio.file import Paths
from java.util import Arrays
from org.apache.lucene.analysis import (Analyzer, CharArraySet,
                                        LowerCaseFilter, StopFilter)
from org.apache.lucene.analysis.en import (EnglishPossessiveFilter,
                                           PorterStemFilter)
from org.apache.lucene.analysis.miscellaneous import SetKeywordMarkerFilter
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.codecs.simpletext import SimpleTextCodec
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import (DirectoryReader, IndexWriter,
                                     IndexWriterConfig)
from org.apache.lucene.queryparser.classic import (MultiFieldQueryParser,
                                                   QueryParser,
                                                   QueryParserBase)
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import *
from org.apache.lucene.store import FSDirectory
from org.apache.pylucene.analysis import (PythonEnglishAnalyzer,
                                          PythonTokenFilter)


class WikiDocument:
    """
    A class to represent a wikipedia document as extracted from the page tag in the wikipedia dump.
    """

    def __init__(self, file):
        """
        Create a document object from a file.
        :param file: the file from which to created an document.
        """

        '''
        This part process the xml file.
        '''
        root = minidom.parse(file)
        for child in root.childNodes[0].childNodes:
            if child.nodeName == 'id':
                self.id = child.firstChild.nodeValue
            elif child.nodeName == 'title':
                self.title = child.firstChild.nodeValue
            elif child.nodeName == 'revision':
                for child2 in child.childNodes:
                    if child2.nodeName == 'text':
                        if child2.firstChild != None:
                            text = child2.firstChild.nodeValue
                        else:
                            text = ''
        self.sections = []
        '''
        Parse the wikipedia content using wiki_extractor to extract section.
        '''
        extractor = wiki_extractor.Extractor('', '', '', '')
        text = extractor.transform(text)
        text = extractor.wiki2text(text)
        text = wiki_extractor.compact(extractor.clean(text))
        text = ["= " + self.title + " ="] + text
        section = None
        for t in text:
            if t.startswith("="):
                if section is not None:
                    self.sections.append(section)
                section = Section(t, '')

            else:
                section.add_text(t)
        self.sections.append(section)


class Section:
    """
    Class to represent a section with a title and the text. The text can be appended.
    """

    def __init__(self, title, text):
        self.title = title.strip("=")
        self.text = text

    def add_text(self, text):
        self.text += "\n" + text
