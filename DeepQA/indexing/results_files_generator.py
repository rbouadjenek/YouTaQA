import os
import sys
import json
import lucene
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.util import Version
from org.apache.lucene.index import IndexWriterConfig, IndexWriter, DirectoryReader
from org.apache.lucene.codecs.simpletext import SimpleTextCodec
from org.apache.lucene.store import FSDirectory
from java.nio.file import Path, Paths
from org.apache.lucene.document import Document, StringField, Field, TextField
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser, QueryParserBase
from org.apache.lucene.analysis import StopwordAnalyzerBase, CharArraySet
from org.apache.lucene.search.similarities import *
from java.util import List, Arrays
from indexer import Indexer
from search import Searcher

class ResultsGenerator:
   
    def __init__(self):
       self.searcher = Searcher()
    # def simpleSearch(searchDir, query, sim):
    #         """
    #         Method that searches through documents using only content_section Field
    #         searchDir : the path to the folder that contains the index.
    #         """
    #         # Now search the index:
    #         analyzer = EnglishAnalyzer(Indexer.ENGLISH_STOP_WORDS_SET)
    #         directory = FSDirectory.open(Paths.get(searchDir))
    #         reader = DirectoryReader.open(directory)
    #         searcher = IndexSearcher(reader)
    #         # Parse a simple query that searches for "text":
    #         parser = QueryParser("content_section", analyzer)
    #         query = parser.parse(QueryParser.escape(query))
    #         searcher.setSimilarity(sim)
    #         hits = searcher.search(query, 1000).scoreDocs
    #         return hits

    # def MultiFieldsSearch(searchDir, query, sim):
    #         """
    #         Method that searches through documents using content_section and title_article Fields
    #         searchDir : the path to the folder that contains the index.
    #         """
    #         # Now search the index:
    #         analyzer = EnglishAnalyzer(Indexer.ENGLISH_STOP_WORDS_SET)
    #         directory = FSDirectory.open(Paths.get(searchDir))
    #         reader = DirectoryReader.open(directory)
    #         searcher = IndexSearcher(reader)
    #         parser = MultiFieldQueryParser(
    #             ["content_section", "title_article"], analyzer)
    #         parser.setDefaultOperator(QueryParserBase.OR_OPERATOR)
    #         query = MultiFieldQueryParser.parse(parser, QueryParser.escape(query))
    #         searcher.setSimilarity(sim)
    #         hits = searcher.search(query, 1000).scoreDocs
    #         return hits

    def question_content(input_file, index_dir, output_file, rank_metric):
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                for par in p['paragraphs']:
                    for q in par["qas"]:
                        hits = self.searcher.simpleSearch(index_dir,q["question"],rank_metric)
                        i = 1
                        for h in hits:
                            output_file.write(q["id"]+" Q0 "+str(h.doc)+" "+str(i)+" "+str(h.score)+" RUN1\n")

    def question_title_content(input_file, index_dir, output_file, rank_metric):
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                title = p["title"]
                for par in p['paragraphs']:
                    for q in par["qas"]:
                        hits = searcher.simpleSearch(index_dir,title +" "+q["question"],rank_metric)
                        i = 1
                        for h in hits:
                            output_file.write(q["id"]+" Q0 "+str(h.doc)+" "+str(i)+" "+str(h.score)+" RUN1\n")

    def question_content_title(input_file, index_dir, output_file, rank_metric):
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                for par in p['paragraphs']:
                    for q in par["qas"]:
                        hits = MultiFieldsSearch(index_dir,q["question"],rank_metric)
                        i = 1
                        for h in hits:
                            output_file.write(q["id"]+" Q0 "+str(h.doc)+" "+str(i)+" "+str(h.score)+" RUN1\n")

    def question_title_content_title(input_file, index_dir, output_file, rank_metric):
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                title = p["title"]
                for par in p['paragraphs']:
                    for q in par["qas"]:
                        hits = MultiFieldsSearch(index_dir,title +" "+q["question"],rank_metric)
                        i = 1
                        for h in hits:
                            output_file.write(q["id"]+" Q0 "+str(h.doc)+" "+str(i)+" "+str(h.score)+" RUN1\n")

def main(argv):
    """
    Main function that read input arguments to lunch the script.
    :param argv:
    :return:
    """
    if not os.path.exists('C:\\trec-eval-results'):
        os.mkdir("C:\\trec-eval-results")
    
    output_file = open("C:\\trec-eval-results\\questionXcontent.txt", 'a+', encoding="utf-8")
    input_file = "C:\\Dataset-SQUAD\\train-v2.0.json"
    index_dir = "C:\\Dataset-indexed-final"
    rank_metric = BM25Similarity()
    Results_generator = ResultsGenerator()
    Results_generator.question_content(input_file, index_dir, output_file, rank_metric)


if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])