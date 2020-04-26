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


class Document:
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
                        text = child2.firstChild.nodeValue
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


class Section:
    """
    Class to represent a section with a title and the text. The text can be appended.
    """

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def add_text(self, text):
        self.text += "\n" + text


class Indexer:
    """
        Class which will define our indexer which contains
        the methods of indexing documents.
    """
    # TODO: adding stopwords to the filter.
    analyzer = RegexTokenizer() | LowercaseFilter() | IntraWordFilter() | StopFilter() | StemFilter()

    def __init__(self, index_dir):
        """

        :param index_dir: the dir where to store the index.
        """
        self.indexDir = index_dir
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)

        # Define a Schema for the index
        self.mySchema = Schema(id_article=ID(stored=True),
                               title_article=TEXT(analyzer=Indexer.analyzer, stored=True),
                               id_section=ID(stored=True),
                               title_section=TEXT(analyzer=Indexer.analyzer, stored=True),
                               content_section=TEXT(analyzer=Indexer.analyzer, stored=True))
        # create the index
        self.myIndex = index.create_in(index_dir, self.mySchema)
        self.writer = self.myIndex.writer(procs=4, limitmb=128, multisegment=True)  # batch writing is faster.

    def index_folder(self, folder2index):
        """

        :param folder2index: the folder to be indexed.
        :return:
        """
        # Browse all the files from root and store the paths
        files = glob.glob(folder2index + '**/*.xml', recursive=True)
        num_lines = len(files)
        print('Start processing....')
        # Iterate in the files paths list
        with tqdm(total=num_lines) as pbar:
            for file in files:
                pbar.update(1)
                doc = Document(file)  # this parse the wikipedia page
                self.index_document(doc)  # this indexes the wikipedia page
        # TODO: check how commit works and check how to close this writer and how to get the number of indexed
        #  documents.
        self.close()
        # print("The total number of documents indexed is " + str(self.writer.searcher().document_number()))

    def index_document(self, doc):
        """

        :param doc: the document to be indexed.
        :return:
        """
        # Method that indexes documents
        i = 0
        for section in doc.sections:
            self.writer.add_document(id_article=doc.id,
                                     title_article=doc.title,
                                     id_section=str(doc.id) + "_" + str(i),
                                     title_section=section.title,
                                     content_section=section.text)
            i += 1

    def close(self):
        # close the index
        self.writer.commit()


def search(searchDir, query):
    """
    Method that searches through documents
    searchDir : the path to the folder that contains the index.
    """
    if index.exists_in(searchDir) is True:
        searchIndex = index.open_dir(searchDir)
        print(type(searchIndex))
        QueryParse = MultifieldParser(["title_article", "content_section"],
                                      schema=Schema(id_article=ID(stored=True),
                                                    title_article=TEXT(analyzer=Indexer.analyzer, stored=True),
                                                    id_section=ID(stored=True),
                                                    title_section=TEXT(analyzer=Indexer.analyzer, stored=True),
                                                    content_section=TEXT(analyzer=Indexer.analyzer, stored=True)),
                                      group=qparser.OrGroup)
        Query = QueryParse.parse(query)
        searcher = searchIndex.searcher(weighting=scoring.BM25F())
        result = searcher.search(Query)

    return result


def main(argv):
    """
    Main function that read input arguments to lunch the script.
    :param argv:
    :return:
    """

    input_dir = ''
    output_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('indexer.py -i <input_folder> -o <output_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('indexer.py -i <input_folder> -o <output_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_dir = arg
            if not os.path.isdir(input_dir):
                print(input_dir + ' does not exist.')
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            output_dir = arg
    if input_dir != '' and output_dir != '':
        the_indexer = Indexer(output_dir)
        the_indexer.index_folder(input_dir)
    else:
        print('indexer.py -i <input_folder> -o <output_folder>')
        sys.exit(2)


if __name__ == "__main__":
    """
    The main function.
    """
    # doc = Document("/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/wikipedia/00/00/00/00000012.xml")
    if len(sys.argv) <= 1:
        sys.argv.append('-i')
        sys.argv.append('/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/wikipedia/')
        sys.argv.append('-o')
        sys.argv.append('/home/reda/NetBeansProjects/DeepQA/index_v1.0/')
    main(sys.argv[1:])
    #results = search('/home/reda/NetBeansProjects/DeepQA/index_v1.0/', 'autism')
    #print(results[0])
