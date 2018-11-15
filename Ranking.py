import json
from Rank import Rank

class Ranking:
    def __init__(self):
        self.rankedList = []

    #Turns msg into rank objects. Adds ranks to rankedList
    def addDocuments(self, ngram, msg):
        for item in msg["documents"]:
            rank = Rank(ngram, item["document_id"], item["pagerank"], item["position"], item["frequency"], item["section"], item["date_created"])
            self.rankedList.append(rank)
        return

    #used to sort rankedList by ID so the ranks can be combined for each id
    def sortByID(self, rank):
        return rank.docID

    #For each docId in rankedList it removes all but the highest totalRank
    #It also combines the matching ngrams
    def combineRanks(self):
        self.rankedList.sort(key=self.sortByID)
        for i in range(len(self.rankedList)-2):
            if self.rankedList[i].docID == self.rankedList[i+1].docID:
                if(self.rankedList[i].totalRank > self.rankedList[i+1].totalRank):
                    self.rankedList[i].addNgram(self.rankedList[i+1].nGram)
                    self.rankedList.pop(i+1)
                else:
                    self.rankedList[i+1].addNgram(self.rankedList[i].nGram)
                    self.rankedList.pop(i)
                continue
        return

    #returns the docID and totalRank for each document
    def getDocuments(self):
        self.combineRanks()
        self.rankedList.sort(reverse=True)
        pages = []
        for doc in self.rankedList:
            pages.append({
                "document_id": doc.docID,
                "keywords" : doc.nGram,
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
    rankings = Ranking()
    rankings.addDocuments("input1", json.load(open('tests/input.json')))
    rankings.addDocuments("input2", json.load(open('tests/input2.json')))
    docs = rankings.getDocuments()
    printJSON(docs)
    return

#test()
