from whoosh import index, writing, scoring, qparser
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from builtins import str
import os.path


class Indexer:
    
    '''
        Class which will define our indexer and which contains 
        the methods of searching and indexing documents
    '''
    
    def __init__(self, indexDir):
        self.indexDir = indexDir
        if not os.path.exists(indexDir):
            os.mkdir(indexDir)

        # Define a Schema for the index
        self.mySchema = Schema(id_article=ID(stored=True),
                          title_article=TEXT(stored=True),
                          id_section=ID(stored=True),
                          title_section=TEXT(stored=True),
                          content_section=TEXT(stored=True))
        # create the index
        self.myIndex = index.create_in(indexDir, self.mySchema)
        self.writer = writing.BufferedWriter(self.myIndex, period=None, limit=1000)

    def indexDocument(self, idArticle, titleArticle, idSection, titleSection, contentSection):
        # Method that indexes documents
        self.writer.add_document(id_article=str(idArticle),
                                 title_article=str(titleArticle),
                                 id_section=str(idSection),
                                 title_section=str(titleSection),
                                 content_section=str(contentSection))
    def close(self):
        # close the index
        self.writer.close()

    def search(self, query):
        # Method that searches through documents
        QueryParse = MultifieldParser(["title_article", "content_section"], schema=self.mySchema, group=qparser.OrGroup)
        Query = QueryParse.parse(query)
        searcher = self.myIndex.searcher(weighting=scoring.BM25F())
        result = searcher.search(Query)

        return result
