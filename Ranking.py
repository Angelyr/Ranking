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


    # @TODO isn't this where the linear combination of the individual ranks should be?
    #combines the ranks of documents with the same docID
    def combineRanks(self):

        # @TODO do we need to sort on "docId" or is this default?
        self.rankedList.sort()

        for i in range(len(self.rankedList)-1):
            
            # If a duplicate id, then pop the smaller one from the list
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

# test()