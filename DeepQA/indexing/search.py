import lucene
from indexer import Indexer
from java.nio.file import Paths
from my_python_english_analyzer import MyPythonEnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import (MultiFieldQueryParser,
                                                   QueryParser,
                                                   QueryParserBase)
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory
from org.apache.pylucene.analysis import PythonEnglishAnalyzer


class Searcher:

    """
    Class that contains the search methods
    """
    def __init__(self, searchDir):
        self.analyzer = MyPythonEnglishAnalyzer(
            stopwords=Indexer.ENGLISH_STOP_WORDS_SET)
        self.directory = FSDirectory.open(Paths.get(searchDir))
        self.reader = DirectoryReader.open(self.directory)
        self.searcher = IndexSearcher(self.reader)
        

    def simpleSearch(self, query, sim):
        """
        Method that searches through documents using only content_section Field
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        parser = QueryParser("content_section", self.analyzer)
        query = parser.parse(QueryParser.escape(query))
        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(query, 1000).scoreDocs
        return hits

    def MultiFieldsSearch(self, query, sim):
        """
        Method that searches through documents using content_section and title_article Fields
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        parser = MultiFieldQueryParser(
            ["content_section", "title_article"], self.analyzer)
        parser.setDefaultOperator(QueryParserBase.OR_OPERATOR)
        query = MultiFieldQueryParser.parse(parser, QueryParser.escape(query))
        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(query, 1000).scoreDocs
        return hits
