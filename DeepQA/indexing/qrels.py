import getopt
import json
import os.path
import sys
from tqdm import tqdm
from search import Searcher
from org.apache.lucene.search.similarities import *


class qrels:
    """
    A class to create the qrels of the questions for SQUAD dataset.
    """

    def __init__(self, index_dir):
        self.searchObject = Searcher(index_dir)

    def get_id_section(self, pair):
        """
        This is the function that returns the id of the passage that is similar to the context.
        :param index_dir: the folder where the dataset index is stored.
        :param input_query: the query that represents the context.
        :return:
        """
        result = self.searchObject.simpleSearch(pair, BM25Similarity())
        id = None
        for i in range(len(result)):
            hitDoc = self.searchObject.searcher.doc(result[i].doc)
            id = hitDoc.get("id_section")
            content = hitDoc.get("content_section")
            if id != "":
                break
        return id, content

    def process(self, input_file, output_dir):
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
                    num_lines += 1

        output_file = open(output_dir + "/qrels.txt", 'a+', encoding="utf-8")
        with tqdm(total=num_lines) as pbar:
            with open(input_file, encoding="utf-8") as json_file:
                data = json.load(json_file)
                for p in data['data']:

                    for par in p['paragraphs']:
                        pbar.update(1)
                        psg_id, content = self.get_id_section(
                            (p['title'], par["context"]))
                        # print("Content: "+content+"\n")
                        similarity = 0
                        for q in par["qas"]:
                            qst_id = q["id"]
                            output_file.write(
                                qst_id + " 0 " + psg_id + " 1 " + str(similarity) + "\n")
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
        opts, args = getopt.getopt(
            argv, "hi:d:o:", ["ifile=", "dfile=", "ofile="])
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
                print(input_file + ' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            output_dir = arg
            if not os.path.isdir(output_dir):
                print(output_dir + ' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-d"):
            index_dir = arg
            if not os.path.isdir(index_dir):
                print(index_dir + ' does not exist.')
                print("\n")
                sys.exit(2)

    if input_file != '' and output_dir != '' and index_dir != '':
        qrelevance = qrels(index_dir)
        qrelevance.process(input_file, output_dir)
    else:
        print('qrels.py -i <input_file> -d <index_dir> -o <output_folder>')
        sys.exit(2)


if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])
