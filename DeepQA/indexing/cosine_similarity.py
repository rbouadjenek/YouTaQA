import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords


class CosineSimilarity:
    STOP_WORDS = stopwords.words('english')

    def clean_string(self, text):
        text = ''.join(
            [word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split()
                         if word not in self.STOP_WORDS])
        return text

    def cosine_sim_vectors(self, vec1, vec2):
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)
        return 100 * cosine_similarity(vec1, vec2)[0][0]

    def similarity(self, string_1, string_2):
        self.sentences = [string_1, string_2]
        cleaned = list(map(self.clean_string, self.sentences))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        cos_Sim = self.cosine_sim_vectors(vectors[0], vectors[1])

        return round(cos_Sim, 2)
