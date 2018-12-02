#Kristine

import datetime
from dateutil import parser

class Rank: 
    # function is called by Rank(nGram, docID, pageRank, position, frequency, section, lastUpdated)
    def __init__(self, nGram, docID, pageRank, position, frequency, section, lastUpdated):
        self.nGram = nGram             # string for the n-gram  
        self.docID = docID             # int for the document ID for this page 
        self.pageRank = pageRank       # int for the document page rank
        self.position = position       # int for the (greatest) position of the n-gram on the page 
        self.frequency = frequency     # int for the frequency of the n-gram on the page 
        self.section = section         # string for the (greatest) section for which the n-gram is located in 
        self.lastUpdated = lastUpdated    # string for the date of when the document was last updated 
        self.weightDict = {}           # dictionary for the weights of each ranking factor
        self.getWeights()
        self.dateScore = self.fixDate()
        self.totalRank = 0            # int for the totalrank for this n-gram and this document 
        

    def __lt__(self, other):
        # less than method that will be used when calling sort()
        return self.totalRank < other.totalRank

    #add Ngram to Rank for the purpose of keywords
    def addNgram(self, ngram):
        if ngram not in self.nGram:
            self.nGram += " " + ngram

    def calculateRankScore(self):
        self.getWeights()
        # calculate the total rank score 
        totalScore = self.getPageRankScore() + self.getPositionScore() + self.getFrequencyScore() + self.getSectionScore() + self.getUpdateScore()
        return totalScore
    
    def getPageRankScore(self):
        # get the page rank for this webpage
        pagerank = self.pageRank
        weight = self.weightDict["pageRank"]
        return pagerank * weight


    def getPositionScore(self):
        # get the position score for the n-gram on this page 
        position = self.position
        weight = self.weightDict["position"]
        return position * weight
    
    def getFrequencyScore(self):
        # get the frequency score for the n-gram on this page
        freq = self.frequency 
        weight = self.weightDict["frequency"]
        return freq * weight
    
    def getSectionScore(self):
        # get the section score for the n-gram on this page 
        weight = self.weightDict["section"]
        if (self.section=='title'):
            return 1 * weight
        elif (self.section == 'description'):
            return 0.9 * weight
        elif (self.section == 'keywords'):
            return 0.8 * weight
        elif (self.section == 'header'):
            return 0.7 * weight
        elif (self.section == 'body'):
            return 0.6 * weight
    
    def fixDate(self):
        # parse the date string into a date object
        dt = parser.parse(self.lastUpdated)
        d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        day_diff = datetime.datetime.now() - d
        return 1/day_diff.days

    def getUpdateScore(self): 
        # get the update score for this webpage
        weight = self.weightDict["lastUpdated"]
        return (self.dateScore * weight)

    def getWeights(self):
        # get weights from the text file -- create a dictionary with the ranking factors as the keys, and the weights as the values 
        file = open("DocFeatureWeights.txt", "r")
        for line in file:
            (key, val) = line.split()
            self.weightDict[key] = float(val)
        file.close()

def test():
    r = Rank('dog', 123, 3.5, 100, 3, 'title', "2018-11-05T16:18:03+0000")
    print(r.getWeights())
    print("Update score:", r.getUpdateScore())
    print("Section score:", r.getSectionScore())
    print("Frequency score:", r.getFrequencyScore())
    print("Page rank score:", r.getPageRankScore())
    print("Position score:", r.getPositionScore())
    print("Total rank score:", r.calculateRankScore())

# test()