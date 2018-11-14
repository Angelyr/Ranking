from flask import Flask, request, jsonify
import time
import requests
from TextProcessing import makeNGrams
from Ranking import parseMsg
from TextProcessing import makeNGrams

app = Flask(__name__)


# Receives the UI team's query and calls getRanking to get ranking results 
@app.route('/search', methods=['GET'])
def recvQuery():
	print(request.args.get('query'))
	
	rankedList = getRanking(request.args.get('query'))
	
	return rankedList
	# return 'Recvieved your query: ' + request.args.get('query')


# Sends the POST Request to index in order to recieve the document features
def sendIndexReq(nGram):
	
	# @TODO make a dummy service/file to spoof the index service
	r = requests.post('https://httpbin.org/post', data = {'key':'value'})
	print(r.content)
	
	return r

# @TODO remove
# #Sends urls to U/I
# def sendUrls(pages):
# 	return


# Call functions in other files to do the business logic of ranking
def getRanking(query):
	
	# Call other file to get the n-grams
	nGrams = makeNgrams(query)

	print(mGrams)

	# for each n-gram, send a query to index

	# Send the nNgrams to the Index team to get the document features
	# r = sendIndexReq(nNgrams)
	r = sendIndexReq(query)

	# collect all the nGramFeatures into a data structure (list of dicts?)
	# nGramFeatures = 

	# sent the result to the ranking class, receive ranked list
	# rankedList = calculateRanks(nGramFeatures)
	# return rankedList



if __name__ == "__main__":
	# @TODO remove debug before production
	app.run(debug=True)
