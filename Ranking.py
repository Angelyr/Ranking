import json
from Rank import Rank

class Ranking:
    #Input: none
    #Output: none
    #SideEffect: initializes arrays for ranks and stats
    #Purpose: used by MessageHandler initialize a Ranking object
    def __init__(self):
        self.rankList = []
        self.statsList = []

    #Input: data in format (nGram,docID,inTitle,_,_,headerFreq,bodyFreq)
    #Output: none
    #SideEffect: adds temp for each item in data
    #Purpose: used by MessageHandler to add documents to rank
    def addNgram(self, data):
        for item in data:
            section = 'body'
            if(item[2] == 't'): section = 'title'
            if(item[5] > 0): section = 'header'
            nGram = item[0]
            docID = item[1]
            pageRank = 0
            position = 0
            frequency = float(item[6])
            date = 0
            temp = (nGram, docID, pageRank, position, frequency, section, date)
            self.statsList.append(temp)
        return

    #Input: data in format (docID,pageRank,date)
    #Output: none
    #SideEffect: adds Rank object to rankList. Ramoves matching docs in statsList
    #Purpose: used by MessageHandler to add documents to rank
    def addMoreStats(self, data):
        for item in list(self.statsList):
            if(data[0] == item[1]):
                nGram = item[0]
                docID = item[1]
                pageRank = float(data[1])
                position = 0
                frequency = float(item[4])
                section = item[5]
                date = str(data[2])
                temp=Rank(nGram, docID, pageRank, position, frequency, section, date)
                self.rankList.append(temp)
                self.statsList.remove(item)
        return


    #Input: rank object
    #Output: the id of the rank object
    #SideEffect: none
    #Purpose: used to sort rankList by ID
    def __sortByID(self, rank):
        return rank.docID

    # normalize the different scores
    def __normalizeScores(self):
        maxPageRank = 0
        minPageRank = 999999
        # maxPosition = 0
        # minPosition = 999999
        maxFrequency = 0
        minFrequency = 999999
        maxDate = 0
        minDate = 999999
        for rank in self.rankList:
            if rank.pageRank > maxPageRank:
                maxPageRank = rank.pageRank
            if rank.pageRank < minPageRank:
                minPageRank = rank.pageRank
            # if rank.position > maxPosition:
            #     maxPosition = rank.position
            # if rank.position < minPosition:
            #     minPosition = rank.position
            if rank.frequency > maxFrequency:
                maxFrequency = rank.frequency
            if rank.frequency < minFrequency:
                minFrequency = rank.frequency
            if rank.dateScore > maxDate:
                maxDate = rank.dateScore
            if rank.dateScore < minDate:
                minDate = rank.dateScore

        for r in self.rankList:
            if maxPageRank != minPageRank:
                r.pageRank = (r.pageRank - minPageRank) / (maxPageRank - minPageRank)
            # r.position = (r.position - minPosition) / (maxPosition - minPosition)
            if maxFrequency != minFrequency: 
                r.frequency = (r.frequency - minFrequency) / (maxFrequency - minFrequency)
            if maxDate != minDate:
                r.dateScore = (r.dateScore - minDate) / (maxDate - minDate)
            r.totalRank = r.calculateRankScore()


    #Input: none
    #Output: none
    #SideEffect: sorts rankList by id and removes ranks with the id that have lower total rank
    #Purpose: used by getDocuments to only return one of each document
    def __combineRanks(self):
        self.rankList.sort(key=self.__sortByID)
        combinedList = []
        for i in range(len(self.rankList)-1):
            #if the IDs match
            if self.rankList[i].docID == self.rankList[i+1].docID:
                #pop the rank with the lower totalRank and combine the nGrams
                self.rankList[i+1].addNgram(self.rankList[i].nGram)
                if(self.rankList[i].totalRank > self.rankList[i+1].totalRank):
                    self.rankList[i+1].totalRank = self.rankList[i].totalRank
            else:
                combinedList.append(self.rankList[i])
        combinedList.append(self.rankList[len(self.rankList)-1])
        self.rankList = combinedList
        return

    #Input: none
    #Output: docID, totalRank, and keywords for each document
    #SideEffect: effects of combineRanks and lists sorted by total rank
    #Purpose: used by message handler to get the list of documents to send to UI
    def getDocuments(self):
        self.__normalizeScores()
        self.__combineRanks()
        self.rankList.sort(reverse=True)
        pages = []

        for doc in self.rankList:
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
    rankings.addNgram([("fish",1,"t","t","t",0.6,1.0),("tropical",1,"t","t","t",0,0)])
    rankings.addNgram([("new",2,"t","t","t",1,1),("word",2,"t","t","t",1,1),("bat",2,"t","t","t",1,1),("man",2,"t","t","t",1,1)])
    rankings.addMoreStats((1,2,"2018-10-05T16:18:03+0000"))
    rankings.addMoreStats((2,3,"2018-11-05T16:18:03+0000"))
    docs = rankings.getDocuments()
    printJSON(docs)
    return
# test()
