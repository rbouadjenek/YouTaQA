import string

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import textdistance


class Similarity:
    """
    A class that caculates string similarity
    """
    STOP_WORDS = stopwords.words('english')

    def clean_string(self, text):
        """
        A function that eliminates stopWords, punctuation and caps
        """
        text = ''.join(
            [word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split()
                         if word not in self.STOP_WORDS])
        return text

    def cos_sim_vectors(self, vec1, vec2):
        """
        Calculate the Cosine Similarity between two vectors
        """
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)
        return 100 * cosine_similarity(vec1, vec2)[0][0]

    def dice_similarity(self, string_1, string_2):
        """
        Calculate the Dice Distance between two string lists
        """
        return textdistance.sorensen(string_1, string_2)

    def jaccard_similarity(self, string_1, string_2):
        """
        Calculate the Jaccard Distance between two string lists
        """
        return textdistance.jaccard(string_1, string_2)

    def cosine_similarity(self, string_1, string_2):
        """
        Calculate the percentage of similarity
        """
        self.sentences = [string_1, string_2]
        cleaned = list(map(self.clean_string, self.sentences))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        cos_Sim = self.cos_sim_vectors(vectors[0], vectors[1])
        return round(cos_Sim, 2)
