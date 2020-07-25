import lucene
import unidecode
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.pylucene.analysis import PythonTokenFilter


class DiacriticFilter(PythonTokenFilter):
    """
    Class of the filter which makes the text in unicode and remove special characters
    """

    def __init__(self, input):
        super().__init__(input)
        self.termAtt = self.addAttribute(CharTermAttribute.class_)
        self.input = input

    def incrementToken(self):
        if self.input.incrementToken():
            text = self.termAtt.toString()
            text = unidecode.unidecode(text)  # This removes accents.
            self.termAtt.setEmpty()
            self.termAtt.append(text)
            return True
        else:
            return False
