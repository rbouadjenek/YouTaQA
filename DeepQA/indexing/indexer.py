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


class Section:
    """
    Class to represent a section with a title and the text. The text can be appended.
    """

    def __init__(self, title, text):
        self.title = title.strip("=")
        self.text = text

    def add_text(self, text):
        self.text += "\n" + text


class Indexer:
    """
        Class which will define our indexer which contains
        the methods of indexing documents.
    """

    def __init__(self, index_dir):
        """

        :param index_dir: the dir where to store the index.
        """
        self.indexDir = index_dir
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(CharArraySet(Arrays.asList(["a", "is", "able"]), False))
        self.analyzer = EnglishAnalyzer(self.ENGLISH_STOP_WORDS_SET)
        self.conf = IndexWriterConfig(self.analyzer)
        self.conf.setUseCompoundFile(False)
        self.directory = FSDirectory.open(Paths.get("index_text/"))


    def index_folder(self, folder2index):
        """

        :param folder2index: the folder to be indexed.
        :return:
        """
        # Browse all the files from root and store the paths
        files = glob.glob(folder2index + '**/*.xml', recursive=True)
        num_lines = len(files)
        print('\n==> Start processing....\n')
        # Iterate in the files paths list
        with tqdm(total=num_lines) as pbar:
            for file in files:
                pbar.update(1)
                doc = WikiDocument(file)  # this parse the wikipedia page
                self.index_document(doc)  # this indexes the wikipedia page
        print("\n==> Please wait ...\n")
        self.close()

    def index_document(self, doc):
        """

        :param doc: the document to be indexed.
        :return:
        """
        # Method that indexes documents
        i = 0
        self.writer = IndexWriter(self.directory, self.conf)
        docu = Document()
        for section in doc.sections:
            docu.add(StringField("id_article", doc.id, Field.Store.YES))
            docu.add(TextField("title_article", doc.title, Field.Store.YES))
            docu.add(StringField("id_section", str(doc.id) + "_" + str(i), Field.Store.YES))
            docu.add(TextField("title_section", section.title, Field.Store.YES))
            docu.add(TextField("content_section", section.text, Field.Store.YES))
            self.writer.addDocument(docu)

            i += 1

    def close(self):
        # close the index
        self.writer.close()


class Searcher:

    def search(self, searchDir, query):
        """
        Method that searches through documents
        searchDir : the path to the folder that contains the index.
        """
        if index.exists_in(searchDir) is True:
            searchIndex = index.open_dir(searchDir)
            QueryParse = MultifieldParser(["title_article", "content_section"], schema=Schema(id_article=ID(stored=True),
                                                                                              title_article=TEXT(
                                                                                                  analyzer=Indexer.analyzer, stored=True),
                                                                                              id_section=ID(
                                                                                                  stored=True),
                                                                                              title_section=TEXT(
                analyzer=Indexer.analyzer, stored=True),
                content_section=TEXT(analyzer=Indexer.analyzer, stored=True)),
                group=qparser.OrGroup)
            Query = QueryParse.parse(query)
            searcher = searchIndex.searcher(weighting=scoring.BM25F())
            result = searcher.search(Query, limit=1)
            return result
        elif index.exists_in(searchDir) is False:
            print("\nNo index found\n")


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
                print("\n")
                print(input_dir + ' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            output_dir = arg
    if input_dir != '' and output_dir != '':
        the_indexer = Indexer(output_dir)
        the_indexer.index_folder(input_dir)
        print("==> Documents successfully indexed \n")
    else:
        print('indexer.py -i <input_folder> -o <output_folder>')
        sys.exit(2)


if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])
