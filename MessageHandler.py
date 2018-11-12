from flask import Flask, request, jsonify
import time
import requests
from TextProcessing import makeNGrams
import Ranking

app = Flask(__name__)


# Receives the UI team's query and calls getRanking to get ranking results 
@app.route('/search', methods=['GET'])
def recvQuery():
	print(request.args.get('query'))
	
	processQuery(request.args.get('query'))
	
	return 'Recvieved your query: ' + request.args.get('query')


def sendIndexReq(nGram):
	r = requests.post('https://httpbin.org/post', data = {'key':'value'})
	print(r.content)
	return r

#Sends urls to U/I
def sendUrls(pages):
	return


# Call functions in other files to do the business logic of ranking
def getRanking(query):
	
	# Call other file to get the n-grams
	# nGrams = getNgrams(query)

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
