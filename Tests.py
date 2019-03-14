import requests
import json

class Tests:

	def __init__(self):
		self.url = "http://localhost:5000/search?query="

	def testQuery(self, queryStr):
		r = requests.get(self.url + queryStr)
		d = json.loads(r.text)
		assert(d['docs'] or d['docs'] == [])
		return d

	def runTestCases(self):

		# one word query 
		result_json = self.testQuery("fish")
		assert(result_json['docs'][0]['docid'] == 1 and result_json['docs'][0]['keywords'] == 'fish')
		assert(result_json['docs'][1]['docid'] == 2 and result_json['docs'][1]['keywords'] == 'fish')
		print("Passed test1")

		result_json = self.testQuery("established to be helpfully")
		# print("Passed test2")

		# empty query 
		result_json = self.testQuery("")
		assert(result_json['docs'] == [])
		print("Passed test3")

		self.testQuery("established to be helpfully")
		# print("Passed test4")

		# query with stop words 
		result_json = self.testQuery("a fish the fish")
		assert(result_json['docs'][0]['docid'] == 1 and result_json['docs'][0]['keywords'] == 'fish the fish')
		assert(result_json['docs'][1]['docid'] == 2 and result_json['docs'][1]['keywords'] == 'fish')
		print("Passed test5")

		self.testQuery("teds tropical fish store established to be helpfully")
		# print("Passed test6")

		# special UTF character 
		result_json = self.testQuery("fish π")
		assert(result_json['docs'][0]['docid'] == 1 and result_json['docs'][0]['keywords'] == 'fish')
		assert(result_json['docs'][1]['docid'] == 2 and result_json['docs'][1]['keywords'] == 'fish')
		print("Passed test7")

		# query longer than maximum length
		queryStr = "fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish "
		r = requests.get(self.url + queryStr)
		d = json.loads(r.text)
		assert(d["error"])
		print("Passed test8")

		# repeated word query 
		result_json = self.testQuery("fish fish")
		assert(result_json['docs'][0]['docid'] == 1 and result_json['docs'][0]['keywords'] == 'fish fish')
		assert(result_json['docs'][1]['docid'] == 2 and result_json['docs'][1]['keywords'] == 'fish')
		print("Passed test9")

		# query longer than 5 words 
		result_json = self.testQuery("domain is established to be used helpfully")
		# print("Passed test10")

		# same query multiple times
		result_json1 = self.testQuery("fish fish")
		result_json2 = self.testQuery("fish fish")
		assert(result_json1['docs'] == result_json2['docs'])
		print("Passed test11")

		# query with 5 gram
		result_json = self.testQuery("established to be used helpfully")
		# print("Passed test12")








t = Tests()
t.runTestCases()
