from indexer import Indexer
from java.nio.file import Paths
from my_python_english_analyzer import MyPythonEnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser, QueryParserBase
from org.apache.lucene.search import BooleanClause, BooleanQuery


from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory


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
        hits = self.searcher.search(query, 5).scoreDocs
        return hits

    def multiFieldsSearch(self, query, sim):
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

    def pairSearch(self, pair, sim):
        """
        Method that searches through documents using only content_section Field
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        title = pair[0].replace('_', ' ')
        content = pair[1]
        parser = QueryParser("content_section", self.analyzer)
        query1 = parser.parse(QueryParser.escape(title))
        query2 = parser.parse(QueryParser.escape(content))

        bq = BooleanQuery.Builder()
        bq.add(query1, BooleanClause.Occur.FILTER)
        bq.add(query2, BooleanClause.Occur.SHOULD)

        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(bq.build(), 1000).scoreDocs
        return hits

    def multiFieldsPairSearch(self, pair, sim):
        """
        Method that searches through documents using only content_section Field
        searchDir : the path to the folder that contains the index.
        """
        # Now search the index:
        title = pair[0].replace('_', ' ')
        content = pair[1]
        parser = MultiFieldQueryParser(
            ["content_section", "title_article"], self.analyzer)
        parser.setDefaultOperator(QueryParserBase.OR_OPERATOR)
        query1 = MultiFieldQueryParser.parse(parser, QueryParser.escape(title))
        query2 = MultiFieldQueryParser.parse(
            parser, QueryParser.escape(content))

        bq = BooleanQuery.Builder()
        bq.add(query1, BooleanClause.Occur.FILTER)
        bq.add(query2, BooleanClause.Occur.SHOULD)

        self.searcher.setSimilarity(sim)
        hits = self.searcher.search(bq.build(), 1000).scoreDocs
        return hits
