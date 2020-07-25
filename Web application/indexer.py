import getopt
import glob
import os
import sys
from tqdm import tqdm
import lucene
from java.nio.file import Paths
from java.util import Arrays
from my_python_english_analyzer import MyPythonEnglishAnalyzer
from org.apache.lucene.analysis import Analyzer, CharArraySet
from org.apache.lucene.codecs.simpletext import SimpleTextCodec
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import *
from org.apache.lucene.store import FSDirectory
from wiki_doc import *


class Indexer:
    """
        Class which will define our indexer which contains
        the methods of indexing documents.
    """
    ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(CharArraySet(Arrays.asList(
        ["a", "a's", "able", "about", "above", "according", "accordingly", "across", "actually", "after",
         "afterwards", "again", "against", "ain't", "all", "allow", "allows", "almost", "alone", "along", "already",
         "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow",
         "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate",
         "are", "aren't", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away",
         "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
         "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both",
         "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", "cannot", "cant", "cause", "causes",
         "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently",
         "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn't",
         "course", "currently", "d", "definitely", "described", "despite", "did", "didn't", "different", "do",
         "does", "doesn't", "doing", "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg",
         "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever",
         "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f",
         "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly",
         "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives", "go",
         "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has",
         "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", "her", "here", "here's",
         "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hither",
         "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "ignored",
         "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar",
         "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "j", "just",
         "k", "keep", "keeps", "kept", "know", "knows", "known", "l", "last", "lately", "later", "latter",
         "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "little", "look",
         "looking", "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
         "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name", "namely", "nd",
         "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine",
         "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere",
         "o", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
         "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside",
         "over", "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus",
         "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re",
         "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "s",
         "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed",
         "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven",
         "several", "shall", "she", "should", "shouldn't", "since", "six", "so", "some", "somebody", "somehow",
         "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified",
         "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", "tell",
         "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs",
         "them", "themselves", "then", "thence", "there", "there's", "thereafter", "thereby", "therefore",
         "therein", "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think",
         "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru",
         "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying",
         "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon",
         "us", "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "very", "via",
         "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've",
         "welcome", "well", "went", "were", "weren't", "what", "what's", "whatever", "when", "whence", "whenever",
         "where", "where's", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",
         "which", "while", "whither", "who", "who's", "whoever", "whole", "whom", "whose", "why", "will", "willing",
         "wish", "with", "within", "without", "won't", "wonder", "would", "would", "wouldn't", "x", "y", "yes",
         "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours"]), False))

    def __init__(self, index_dir):
        """

        :param index_dir: the dir where to store the index.
        """
        self.indexDir = index_dir
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        self.analyzer = MyPythonEnglishAnalyzer(
            stopwords=self.ENGLISH_STOP_WORDS_SET)
        conf = IndexWriterConfig(self.analyzer)
        conf.setUseCompoundFile(False)
        directory = FSDirectory.open(Paths.get(index_dir))
        self.writer = IndexWriter(directory, conf)

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
        self.writer.commit()
        print('A total of ' + str(self.writer.getDocStats().numDocs) +
              ' have been indexed.')
        self.close()

    def index_document(self, wiki_doc):
        """
        :param wiki_doc: the document to be indexed.
        :return:
        """
        # Method that indexes documents
        i = 0
        for section in wiki_doc.sections:
            doc = Document()
            doc.add(StringField("id_article", wiki_doc.id, Field.Store.YES))
            doc.add(TextField("title_article", wiki_doc.title, Field.Store.YES))
            doc.add(StringField("id_section", str(
                wiki_doc.id) + "_" + str(i), Field.Store.YES))
            doc.add(TextField("title_section", section.title, Field.Store.YES))
            doc.add(TextField("content_section", section.text, Field.Store.YES))
            self.writer.addDocument(doc)
            i += 1

    def close(self):
        # close the index
        self.writer.close()


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
