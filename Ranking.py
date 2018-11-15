import json
from Rank import Rank

class Ranking:
    def __init__(self):
        self.rankedList = []

    #Input: ngram string and JSON message
    #Output: none
    #SideEffect: adds rank to rankedList for each document in msg
    #Purpose: used by MessageHandler to add documents to rank
    def addDocuments(self, ngram, msg):
        for item in msg["documents"]:
            rank = Rank(ngram, item["document_id"], item["pagerank"], item["position"], item["frequency"], item["section"], item["date_created"])
            self.rankedList.append(rank)
        return

    #Input: rank object
    #Output: the id of the rank object
    #SideEffect: none
    #Purpose: used to sort rankedList by ID
    def __sortByID(self, rank):
        return rank.docID

    #Input: none
    #Output: none
    #SideEffect: sorts rankedList by id and removes ranks with the id that have lower total rank
    #Purpose: used by getDocuments to only return one of each document
    def __combineRanks(self):
        self.rankedList.sort(key=self.__sortByID)
        for i in range(len(self.rankedList)-2):
            #if the IDs match
            if self.rankedList[i].docID == self.rankedList[i+1].docID:
                #pop the rank with the lower totalRank and combine the nGrams
                if(self.rankedList[i].totalRank > self.rankedList[i+1].totalRank):
                    self.rankedList[i].addNgram(self.rankedList[i+1].nGram)
                    self.rankedList.pop(i+1)
                else:
                    self.rankedList[i+1].addNgram(self.rankedList[i].nGram)
                    self.rankedList.pop(i)
                continue
        return

    #Input: none
    #Output: docID, totalRank, and keywords for each document
    #SideEffect: effects of combineRanks and lists sorted by total rank
    #Purpose: used by message handler to get the list of documents to send to UI
    def getDocuments(self):
        self.__combineRanks()
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

#Input: JSON string
#Output: none
#SideEffect: prints JSON string
#Purpose: prints JSON in format that is easier to read
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
