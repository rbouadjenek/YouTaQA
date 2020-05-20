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
<<<<<<< HEAD
    searchObject = Searcher("C:\Dataset-indexed-final")
    result = searchObject.MultiFieldsSearch(inputQuery, BM25Similarity())
=======
    searchObject = Searcher()
    result = searchObject.MultiFieldsSearch(
        "/Users/younesagabi/Desktop/DeepQA/index_wiki_v7.0", inputQuery, BM25Similarity())
>>>>>>> 9b89498e42513f33646a05a3ccc91b8946db00cc

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
