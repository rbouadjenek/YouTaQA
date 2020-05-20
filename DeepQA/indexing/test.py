import lucene
import wiki_extractor
from org.apache.lucene.search.similarities import *
from search import Searcher
from similarity import Similarity

inputQuery = ""
Similarity = Similarity()

while inputQuery != "exit":
    inputQuery = input("Enter your request, otherwise tape 'exit' to exit\n")
    if inputQuery == "exit":
        break

    searchObject = Searcher("/Users/younesagabi/Desktop/DeepQA/DeepQA/indexing/index")
    result = searchObject.MultiFieldsSearch(inputQuery, BM25Similarity())

    print("#" * 100)
    print("#" * 100)
    content = ""
    for i in range(len(result)):
        hitDoc = searchObject.searcher.doc(result[i].doc)
        score = result[i].score
        content = hitDoc.get("content_section")
        if content != "":
            break
    searchObject.reader.close()
    searchObject.directory.close()
    print("score =>>", score)
    print(content)
    print("#" * 50)
    CosSim = Similarity.cosine_similarity(inputQuery, content)
    jacSim = Similarity.jaccard_similarity(inputQuery, content)
    diceSim = Similarity.dice_similarity(inputQuery, content)
    print("=> Cosiane similarity : ", CosSim)
    print("=> Jaccard similarity : ", jacSim)
    print("=> Dice similarity : ", diceSim)
    print("#" * 50)
