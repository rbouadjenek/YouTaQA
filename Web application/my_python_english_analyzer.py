import lucene
from diactritic_filter import DiacriticFilter
from java.util import Arrays
from org.apache.lucene.analysis import (Analyzer, CharArraySet,
                                        LowerCaseFilter, StopFilter)
from org.apache.lucene.analysis.en import (EnglishPossessiveFilter,
                                           PorterStemFilter)
from org.apache.lucene.analysis.miscellaneous import SetKeywordMarkerFilter
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.search.similarities import *
from org.apache.pylucene.analysis import PythonEnglishAnalyzer

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# lucene.getVMEnv().attachCurrentThread()

class MyPythonEnglishAnalyzer(PythonEnglishAnalyzer):
    """
    Class of our custom analyzer that uses filters:
        -StandardTokenizer.
        -EnglishPossessiveFilter.
        -LowerCaseFilter.
        -DiacriticFilter.
        -StopFilter.
        -SetKeywordMarkerFilter
    """

    ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(CharArraySet(Arrays.asList(
        ["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not",
         "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was",
         "will", "with"]), False))

    def __init__(self, stopwords=ENGLISH_STOP_WORDS_SET, stemExclusionSet=CharArraySet.EMPTY_SET):
        super().__init__(self, stopwords)
        self.stopwords = stopwords
        self.stemExclusionSet = stemExclusionSet

    def createComponents(self, fieldName):
        source = StandardTokenizer()
        result = EnglishPossessiveFilter(source)
        result = LowerCaseFilter(result)
        result = DiacriticFilter(result)
        result = StopFilter(result, self.stopwords)
        if self.stemExclusionSet.isEmpty() is False:
            result = SetKeywordMarkerFilter(result, self.stemExclusionSet)
        result = PorterStemFilter(result)
        return Analyzer.TokenStreamComponents(source, result)

    def normalize(self, fieldName, input):
        return LowerCaseFilter(input)
