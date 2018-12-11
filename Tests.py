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

		self.testQuery("fish")
		print("Passed test1")

		self.testQuery("established to be helpfully")
		print("Passed test2")

		self.testQuery("")
		print("Passed test3")

		self.testQuery("established to be helpfully")
		print("Passed test4")

		self.testQuery("a fish the fish")
		print("Passed test5")

		self.testQuery("teds tropical fish store established to be helpfully")
		print("Passed test6")

		self.testQuery("fish π")
		print("Passed test7")

		queryStr = "fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish fish "
		r = requests.get(self.url + queryStr)
		d = json.loads(r.text)
		assert(d["error"])
		print("Passed test8")






t = Tests()
t.runTestCases()
