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
        # initialize fields 
        self.totalRank = 0             # int for the totalrank for this n-gram and this document 
        self.weightDict = {}           # dictionary for the weights of each ranking factor 

    def _lt_(self, other):
        # less than method that will be used when calling sort()
        return self.totalRank < other.totalRank

    def calculateRankScore(self):
        self.getWeights()
        # calculate the total rank score 
        return self.getPageRankScore() + self.getPositionScore() + self.getFrequencyScore() + self.getSectionScore() + self.getUpdateScore()
    
    def getPageRankScore(self):
        # get the page rank for this webpage
        weight = self.weightDict["pageRank"]
        return weight * self.pageRank


    def getPositionScore(self):
        # get the position score for the n-gram on this page 
        weight = self.weightDict["position"]
        return self.position * weight
    
    def getFrequencyScore(self):
        # get the frequency score for the n-gram on this page
        weight = self.weightDict["frequency"]
        return self.frequency * weight
    
    def getSectionScore(self):
        # get the section score for the n-gram on this page 
        weight = self.weightDict["section"]
        if (self.section=='title'):
            return 10 * weight
        elif (self.section == 'header'):
            return 8 * weight
        elif (self.section == 'body'):
            return 5 * weight
    
    def getUpdateScore(self): 
        # get the update score for this webpage
        weight = self.weightDict["lastUpdated"]

        # parse the date string into a date object
        dt = parser.parse(self.lastUpdated)
        d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        day_diff = datetime.datetime.now() - d
        return (day_diff.days * weight)

    def getWeights(self):
        # get weights from the text file -- create a dictionary with the ranking factors as the keys, and the weights as the values 
        file = open("DocFeatureWeights.txt", "r")
        for line in file:
            (key, val) = line.split()
            self.weightDict[key] = float(val)
        file.close()


r = Rank('dog', 123, 3.5, 150, 3, 'title', "2018-11-05T16:18:03+0000")
print(r.getWeights())
print("Update score:", r.getUpdateScore())
print("Section score:", r.getSectionScore())
print("Frequency score:", r.getFrequencyScore())
print("Page rank score:", r.getPageRankScore())
print("Position score:", r.getPositionScore())
print("Total rank score:", r.calculateRankScore())

