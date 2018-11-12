import json
import threading
from Rank import Rank

rankedList = []

#receives documents from rest layer. Turns it into rank objects. Adds it to rankedList
def parseMsg(ngram, msg):
    for item in data["documents"]:
        rank = Rank(ngram, item["document_id"], item["pagerank"], item["position"], item["frequency"], item["section"], item["date_created"])
        rankedList.append(rank)
    return


#combines the ranks of documents with the same docID
def combineRanks():
    rankedList.sort()
    for i in range(len(rankedList)-1):
        if rankedList[i].docID == rankedList[i+1].docID:
            if(rankedList[i].totalRank > rankedList[i+1].totalRank):
                rankedList.pop(i+1)
            else:
                rankedList.pop(i)
            continue
    sendDocuments()
    return

#sends the urls to the message sender
def sendDocuments():
    pages = []
    for doc in rankedList:
        pages.append({
            "document_id": doc.docID,
            "rank": doc.totalRank
        })
    pages = {
        "pages": pages
    }
    printJSON(pages)
    return pages

#prints JSON in format that is easier to read
def printJSON(data):
    print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
    return


fp = open('input.json')
data = json.load(fp)
parseMsg("hello",data)
combineRanks()

#msg = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#parseMsg(msg)