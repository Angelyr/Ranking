from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def recvQuery():
	print(request.form['query'])
	return 'Received'