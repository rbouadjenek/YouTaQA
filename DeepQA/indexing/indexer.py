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

    CustomStopList = frozenset(["a", "a's", "able",
                "about", "above", "according", "accordingly", "across",
                "actually", "after", "afterwards", "again", "against", "ain't",
                "all", "allow", "allows", "almost", "alone", "along",
                "already", "also", "although", "always", "am", "among",
                "amongst", "an", "and", "another", "any", "anybody", "anyhow",
                "anyone", "anything", "anyway", "anyways", "anywhere", "apart",
                "appear", "appreciate", "appropriate", "are", "aren't",
                "around", "as", "aside", "ask", "asking", "associated", "at",
                "available", "away", "awfully", "b", "be", "became", "because",
                "become", "becomes", "becoming", "been", "before",
                "beforehand", "behind", "being", "believe", "below", "beside",
                "besides", "best", "better", "between", "beyond", "both",
                "brief", "but", "by", "c", "c'mon", "c's", "came", "can",
                "can't", "cannot", "cant", "cause", "causes", "certain",
                "certainly", "changes", "clearly", "co", "com", "come",
                "comes", "concerning", "consequently", "consider",
                "considering", "contain", "containing", "contains",
                "corresponding", "could", "couldn't", "course", "currently",
                "d", "definitely", "described", "despite", "did", "didn't",
                "different", "do", "does", "doesn't", "doing", "don't", "done",
                "down", "downwards", "during", "e", "each", "edu", "eg",
                "eight", "either", "else", "elsewhere", "enough", "entirely",
                "especially", "et", "etc", "even", "ever", "every",
                "everybody", "everyone", "everything", "everywhere", "ex",
                "exactly", "example", "except", "f", "far", "few", "fifth",
                "first", "five", "followed", "following", "follows", "for",
                "former", "formerly", "forth", "four", "from", "further",
                "furthermore", "g", "get", "gets", "getting", "given", "gives",
                "go", "goes", "going", "gone", "got", "gotten", "greetings",
                "h", "had", "hadn't", "happens", "hardly", "has", "hasn't",
                "have", "haven't", "having", "he", "he's", "hello", "help",
                "hence", "her", "here", "here's", "hereafter", "hereby",
                "herein", "hereupon", "hers", "herself", "hi", "him",
                "himself", "his", "hither", "hopefully", "how", "howbeit",
                "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if",
                "ignored", "immediate", "in", "inasmuch", "inc", "indeed",
                "indicate", "indicated", "indicates", "inner", "insofar",
                "instead", "into", "inward", "is", "isn't", "it", "it'd",
                "it'll", "it's", "its", "itself", "j", "just", "k", "keep",
                "keeps", "kept", "know", "knows", "known", "l", "last",
                "lately", "later", "latter", "latterly", "least", "less",
                "lest", "let", "let's", "like", "liked", "likely", "little",
                "look", "looking", "looks", "ltd", "m", "mainly", "many",
                "may", "maybe", "me", "mean", "meanwhile", "merely", "might",
                "more", "moreover", "most", "mostly", "much", "must", "my",
                "myself", "n", "name", "namely", "nd", "near", "nearly",
                "necessary", "need", "needs", "neither", "never",
                "nevertheless", "new", "next", "nine", "no", "nobody", "non",
                "none", "noone", "nor", "normally", "not", "nothing", "novel",
                "now", "nowhere", "o", "obviously", "of", "off", "often", "oh",
                "ok", "okay", "old", "on", "once", "one", "ones", "only",
                "onto", "or", "other", "others", "otherwise", "ought", "our",
                "ours", "ourselves", "out", "outside", "over", "overall",
                "own", "p", "particular", "particularly", "per", "perhaps",
                "placed", "please", "plus", "possible", "presumably",
                "probably", "provides", "q", "que", "quite", "qv", "r",
                "rather", "rd", "re", "really", "reasonably", "regarding",
                "regardless", "regards", "relatively", "respectively", "right",
                "s", "said", "same", "saw", "say", "saying", "says", "second",
                "secondly", "see", "seeing", "seem", "seemed", "seeming",
                "seems", "seen", "self", "selves", "sensible", "sent",
                "serious", "seriously", "seven", "several", "shall", "she",
                "should", "shouldn't", "since", "six", "so", "some",
                "somebody", "somehow", "someone", "something", "sometime",
                "sometimes", "somewhat", "somewhere", "soon", "sorry",
                "specified", "specify", "specifying", "still", "sub", "such",
                "sup", "sure", "t", "t's", "take", "taken", "tell", "tends",
                "th", "than", "thank", "thanks", "thanx", "that", "that's",
                "thats", "the", "their", "theirs", "them", "themselves",
                "then", "thence", "there", "there's", "thereafter", "thereby",
                "therefore", "therein", "theres", "thereupon", "these", "they",
                "they'd", "they'll", "they're", "they've", "think", "third",
                "this", "thorough", "thoroughly", "those", "though", "three",
                "through", "throughout", "thru", "thus", "to", "together",
                "too", "took", "toward", "towards", "tried", "tries", "truly",
                "try", "trying", "twice", "two", "u", "un", "under",
                "unfortunately", "unless", "unlikely", "until", "unto", "up",
                "upon", "us", "use", "used", "useful", "uses", "using",
                "usually", "uucp", "v", "value", "various", "very", "via",
                "viz", "vs", "w", "want", "wants", "was", "wasn't", "way",
                "we", "we'd", "we'll", "we're", "we've", "welcome", "well",
                "went", "were", "weren't", "what", "what's", "whatever",
                "when", "whence", "whenever", "where", "where's", "whereafter",
                "whereas", "whereby", "wherein", "whereupon", "wherever",
                "whether", "which", "while", "whither", "who", "who's",
                "whoever", "whole", "whom", "whose", "why", "will", "willing",
                "wish", "with", "within", "without", "won't", "wonder",
                "would", "would", "wouldn't", "x", "y", "yes", "yet", "you",
                "you'd", "you'll", "you're", "you've", "your", "yours"])

    analyzer = RegexTokenizer() | LowercaseFilter() | IntraWordFilter(splitwords=True, splitnums=True) | StopFilter(stoplist= CustomStopList, lang="en") | StemFilter()

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

        self.close()

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

class Searcher:

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
    main(sys.argv[1:])
