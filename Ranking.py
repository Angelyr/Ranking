import json
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
    for i in range(len(rankedList)-1):
        if rankedList[i].docID == rankedList[i+1].docID:
            if(rankedList[i].totalRank > rankedList[i+1].totalRank):
                rankedList.pop(i+1)
            else:
                rankedList.pop(i)
            continue
    sendDocuments()
    return

#temp
def sendUrls(pages):
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
    sendUrls(pages)
    return

#Testing Purposes
data = {
    "documents":[
        {
            "document_id" : 1,
			"url" : "1",
			"pagerank": 1.0,
			"frequency": 1,
			"position" : 1,
			"date_created" : "1",
			"date_updated" : "1",
			"section" : "1"
        },
        {
            "document_id" : 1,
			"url" : "2",
			"pagerank": 2.0,
			"frequency": 2,
			"position" : 2,
			"date_created" : "2",
			"date_updated" : "2",
			"section" : "2"
        }
    ]
}
parseMsg("hello",data)
combineRanks()

#msg = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#parseMsg(msg)