from flask import Flask, request, jsonify
import time
import requests
import json

from TextProcessing import makeNGrams
from Ranking import Ranking

# for postgres index team
import psycopg2
import pprint

# for spoofing index
import random
random.seed(500)


app = Flask(__name__)


# Receives the UI team's query and calls getRanking to get ranking results 
@app.route('/search', methods=['GET'])
def recvQuery():
	print(request.args.get('query'))
	
	rankedList = getRanking(request.args.get('query'))
	
	return jsonify(rankedList)


# Dummy endpoint for spoofing index service
@app.route('/index', methods=['POST'])
def spoofIndex():

	print(request.form)

	spoofFeatures = {}

	spoofFeatures['document_id'] = random.randint(1,10000)
	spoofFeatures['pagerank'] =	random.random()
	spoofFeatures['position'] = random.random()
	spoofFeatures['frequency'] = random.random()
	spoofFeatures['section'] = "body"
	spoofFeatures['date_created'] = "2018-11-05T16:18:03+0000"

	spoofDocuments = {}
	spoofDocuments["documents"] = []
	spoofDocuments["documents"].append(spoofFeatures)

	return jsonify(spoofDocuments)




# Call functions in other files to do the business logic of ranking
def getRanking(query):
	
	# Call other file to get the n-grams
	ngrams = makeNGrams(query)

	print(ngrams)

	# create a ranking class to keep track of the ngram features
	ranking = Ranking()

	# for each n-gram, send a query to index
	for ngram in ngrams:

		# Send the nNgrams to the Index team to get the document features
		r = sendIndexReq( " ".join(ngram) )

		# @TODO parse the response and handle error 
		parsedMsg = json.loads(r.text)

		print("parsedMsg:")
		print(parsedMsg)

		ranking.addDocuments(ngram, parsedMsg)


	# Calculate the ranks within the ranking class
	ranking.combineRanks()
	rankedList = ranking.getDocuments()

	return rankedList


# Sends the post request to the index team to return the document features for the given ngram
def sendIndexReq(nGram):
	
	print(nGram)

	sql = "SELECT * FROM index WHERE ngram='" + nGram + "';"

	# @TODO fix port, and see if we need to protect against sql injections
	r = requests.post('http://localhost:5000/index', data = {'sql':sql})

	# @TODO error handling


	# connect to postgresql index team
	conn_string = "host='green-z.cs.rpi.edu' dbname='index' user='ranking' password='ranking'"

	conn = psycopg2.connect(conn_string)

	cursor = conn.cursor()


	cursor.execute(sql)

	records = cursor.fetchall()

	pprint.pprint(records)

	return r






if __name__ == "__main__":
	# @TODO remove debug before production
	app.run(debug=True, host='0.0.0.0', port=5000)
