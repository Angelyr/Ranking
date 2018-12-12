#removes all punctuation excluding spaces
def removePuctuation(word):
    for i in range(len(word)):
        if not word[i].isalnum() and not word[i].isspace():
            word = word[:i] + " " + word[i+1:]
    return word

#returns a list of ngrams of sizes 1-5 with and without punctuation
def makeNGrams(query):
    for word in removePuctuation(query).split():
        if word not in query.split():
            query += " " + word

    words = query.split()
    output = []
    for n in range(1,5):
        for i in range(len(words)-n+1):
            output.append(words[i:i+n])
    return output

#testing
def test():
    test = 'How to change the world? in 20.5 days'
    for ngram in makeNGrams(test):
        print(ngram)

test()