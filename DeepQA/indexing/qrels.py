import json
import getopt
import glob
import os
import os.path
import sys
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

class qrels:
    """
    A class to create the qrels of the questions for SQUAD dataset.
    """
    def __init__(self):
        super().__init__()

    def get_id_section(index_dir, input_query):
        """
        This is the function that returns the id of the passage that is similar to the context.
        :param index_dir: the folder where the dataset index is stored.
        :param input_query: the query that represents the context.
        :return:
        """
        searchObject = Searcher()
        result = searchObject.search(index_dir, input_query)
        for i in range(len(result)):
            hitDoc = searchObject.searcher.doc(result[i].doc)
            id = hitDoc.get("id_section")
            if id != "":
                break
        searchObject.reader.close()
        searchObject.directory.close()
        return id
    
    def process(input_file, index_dir, output_dir):
        """
        This is the main function that creates the qrels file.
        :param input_file: the file to process.
        :param index_dir: the folder where the dataset index is stored.
        :param output_dir: the folder where to store the qrels file.
        :return:
        """
        num_lines = 0
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                for par in p['paragraphs']:
                    num_lines += 1;

        output_file = open(output_dir+"./qrels.txt", 'a+', encoding="utf-8")
        with tqdm(total=num_lines) as pbar:
            with open(input_file, encoding="utf-8") as json_file:
                data = json.load(json_file)
                for p in data['data']:
                    for par in p['paragraphs']:
                        pbar.update(1)
                        psg_id = qrels.get_id_section(index_dir, par["context"])
                        for q in par["qas"]:
                            qst_id = q["id"]
                            output_file.write(qst_id+" 0 "+psg_id+" 1\n")
                print("==> Qrels successfully created.\n")

def main(argv):
    """
    Main function that read input arguments to lunch the script.
    :param argv:
    :return:
    """

    input_file = ''
    output_dir = ''
    index_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:o:", ["ifile=", "dfile=", "ofile="])
    except getopt.GetoptError:
        print('qrels.py -i <input_file> -d <index_dir> -o <output_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('qrels.py -i <input_file> -d <index_dir> -o <output_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            if not os.path.isfile(input_file):
                print(input_file+' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            output_dir = arg
            if not os.path.isdir(output_dir):
                print(output_dir+' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-d"):
            index_dir = arg
            if not os.path.isdir(index_dir):
                print(index_dir+' does not exist.')
                print("\n")
                sys.exit(2)

    if input_file != '' and output_dir != '' and index_dir != '':
        qrels.process(input_file, index_dir, output_dir)
    else:
        print('qrels.py -i <input_file> -d <index_dir> -o <output_folder>')
        sys.exit(2)

if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])