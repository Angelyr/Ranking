#removes all punctuation excluding spaces
def removePuctuation(word):
    for i in range(len(word)):
        if not word[i].isalnum() and not word[i].isspace():
            word = word[:i] + " " + word[i+1:]
    return word

#returns a list of ngrams of sizes 1-5 with and without punctuation
def makeNGrams(query):
    if query is None: return []
    query += " " + removePuctuation(query)
    words = query.split()
    output = []
    for n in range(1,6):
        for i in range(len(words)-n+1):
            output.append(words[i:i+n])
    return output

#testing
def test():
    print("test 1:")
    test = ''
    print(makeNGrams(test))

    print("test 2:")
    test = '     '
    print(makeNGrams(test))

    print("test 3:")
    print(makeNGrams(None))

    print("test 4:")
    test = 'A'
    print(makeNGrams(test))

    print("test 5:")
    test = 'A B C D E'
    print(makeNGrams(test))

    print("test 6:")
    test = 'A B C D E F G H I'
    print(makeNGrams(test))

    print("test 7:")
    test = 'A? B! C@ D$ E%'
    print(makeNGrams(test))

    print("test 8:")
    test = 'How to change the world? in 20.5 days'
    print(makeNGrams(test))