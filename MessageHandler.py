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


# Global psql connection vars
# connect to postgresql index team
conn_string = "host='green-z.cs.rpi.edu' dbname='index' user='ranking' password='ranking'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


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

	ids = set()

	# for each n-gram, send a query to index
	for ngram in ngrams:

		# Send the nNgrams to the Index team to get the document features
		records = sendIndexReq( " ".join(ngram) )

		ranking.addNgram(records)

		# loop through the results and add the stats to Ranking class
		for record in records:
			# save the document id so we can get more statistics in a separate call
			ids.add(record[1])

	additionalStatList = sendIndexDocumentReq(ids)
	for additionalStat in additionalStatList:
		ranking.addMoreStats(additionalStat)



	# Calculate the ranks within the ranking class
	rankedList = ranking.getDocuments()

	return rankedList


# Sends the post request to the index team to return the document features for the given ngram
def sendIndexReq(nGram):
	
	print(nGram)

	sql = "SELECT * FROM index WHERE ngram='" + nGram + "';"

	# @TODO remove spoofing 
	# r = requests.post('http://localhost:5000/index', data = {'sql':sql})

	cursor.execute(sql)

	records = cursor.fetchall()

	# pprint.pprint(records)

	return records


def sendIndexDocumentReq(ids):

	idStrList = ","
	idStrList = idStrList.join( list( map(str, ids) ) )

	# @TODO determine if should use regular pagerank or norm_pagerank
	sql = "SELECT id, pagerank, date_updated FROM documents WHERE id IN (" + idStrList + ");"
	# sql = "SELECT id, norm_pagerank, date_updated FROM documents WHERE id IN (" + idStrList + ");"

	cursor.execute(sql)

	records = cursor.fetchall()

	return records



if __name__ == "__main__":
	# @TODO remove debug before production
	app.run(debug=True, host='0.0.0.0', port=5000)
