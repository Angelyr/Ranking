import json
import threading
from Rank import Rank

class Ranking:
    def __init__(self):
        self.rankedList = []

    #receives documents from rest layer. Turns it into rank objects. Adds it to rankedList
    def addDocuments(self, ngram, msg):
        for item in msg["documents"]:
            rank = Rank(ngram, item["document_id"], item["pagerank"], item["position"], item["frequency"], item["section"], item["date_created"])
            self.rankedList.append(rank)
        return


    #combines the ranks of documents with the same docID
    def combineRanks(self):
        self.rankedList.sort()
        for i in range(len(self.rankedList)-1):
            if self.rankedList[i].docID == self.rankedList[i+1].docID:
                if(self.rankedList[i].totalRank > self.rankedList[i+1].totalRank):
                    self.rankedList.pop(i+1)
                else:
                    self.rankedList.pop(i)
                continue
        return

    #sends the urls to the message sender
    def getDocuments(self):
        self.combineRanks()
        pages = []
        for doc in self.rankedList:
            pages.append({
                "document_id": doc.docID,
                "rank": doc.totalRank
            })
        pages = {
            "pages": pages
        }
        return pages

#prints JSON in format that is easier to read
def printJSON(data):
    print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
    return

#Testing purposes
def test():
    data = json.load(open('input.json'))
    rankings = Ranking()
    rankings.addDocuments("hello", data)
    docs = rankings.getDocuments()
    printJSON(docs)
    return

test()