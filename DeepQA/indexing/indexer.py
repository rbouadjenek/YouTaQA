from whoosh import index, writing, scoring, qparser
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser
from builtins import str
import os.path
import os
import glob
import hashlib
from tqdm import tqdm
from xml.dom import minidom
import fileinput
import wiki_extractor
import sys

class Document:
    def __init__(self, file):
        root = minidom.parse(file)
        self.title = getText(root.getElementsByTagName('title'))
        self.id = getText(root.getElementsByTagName('id'))
        self.text = getText(root.getElementsByTagName('text'))

        input_file = file
        file = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)
        for page_data in wiki_extractor.pages_from(file):
            id, revid, title, ns, catSet, page = page_data
            t = wiki_extractor.Extractor(id, revid, title, page)
            print(t.text)





def getText(nodelist):
    # Iterate all Nodes aggregate TEXT_NODE
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        else:
            # Recursive
            rc.append(getText(node.childNodes))
    return ''.join(rc)


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

    def index_folder(self, folder2index):
        # Browse all the files from root and store the paths
        files = glob.glob(folder2index + '**/*.xml', recursive=True)
        num_lines = len(files)

        j = 0
        print('Start processing....')
        # Iterate in the files paths list
        with tqdm(total=num_lines) as pbar:
            for file in files:  # saint-austin / Brazilian
                pbar.update(1)
                j += 1
                # Extract file name
                doc = Document(file)
            indexer.close

    def indexDocument(self, doc):
        # Method that indexes documents
        self.writer.add_document(id_article=doc.id,
                                 title_article=doc.title,
                                 id_section='',
                                 title_section=doc.title,
                                 content_section=doc.text)

    def close(self):
        # close the index
        self.writer.close()


if __name__ == "__main__":
    # main()
    doc = Document("/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/wikipedia/00/00/00/00000012.xml")
    #indexer = Indexer("/home/reda/NetBeansProjects/DeepQA/index_v1.0")
    #indexer.index_folder("/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/wikipedia/00/00/")
