#returns a list of ngrams of sizes 1-5
def makeNGrams(query):
    words = query.split()
    output = []
    for n in range(1,5):
        for i in range(len(words)-n+1):
            output.append(words[i:i+n])
    return output

#testing
def test():
    test = 'How to change the world in 20 days'
    for ngram in makeNGrams(test):
        print(ngram)

