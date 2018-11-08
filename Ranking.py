import json
#from Rank import Rank
#from MessageSender import sendUrls

print('Ranking is now running')
rankedList = []

#receives msg from rest layer
def parseMsg(ngram, msg):
    for item in data["documents"]:
        rank = temp(ngram, item["document_id"], item["pagerank"], item["frequency"], item["position"], item["date_created"], item["date_updated"], item["section"])

        rankedList.append(rank)
        print(rankedList)
    return

def temp(a,b,c,d,e,f,g,h):
    return (a,b,c,d,e,f,g,h)

#combines the ranks of documents with the same url
def combineRanks():
    for i in range(len(rankedList)-1):
        if rankedList[i][1] == rankedList[i+1][1]:
            if(rankedList[i][1] > rankedList[i+1][1]):
                rankedList.pop(i+1)
            else
                rankedList.pop(i)
             
    return

#sends the urls to the message sender
def sendDocuments():
    return

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
            "document_id" : 2,
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
#msg = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#parseMsg(msg)