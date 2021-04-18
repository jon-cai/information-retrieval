from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import math
import re


def startSearch():
    ps = PorterStemmer()
    try:
        with open("indexindex.txt", "r") as ind:
            ind2 = eval(ind.readline())
        with open("url_index.txt", "r") as urlfile:
            url_id = eval(urlfile.readline())
    except FileNotFoundError:
        print("inverted index incomplete.")
        return

    invfile = open("finalindex.txt", "r")
    while 1:
        search = input("search>>> ")
        if search == "exit":
            while 1:
                confirm = input("Exit search engine? (Y/N): ")
                if confirm.lower() == "y":
                    return
                elif confirm.lower() == "n":
                    break  # user doesn't want to exit; return results for the query "exit"
        start = time.time()
        terms = defaultdict(int)
        for term in search.split():
            if not re.match('[A-Za-z0-9]+', term):
                continue
            terms[ps.stem(term.lower())] += 1

        if len(terms) == 0:
            continue

        lookup = indexLookup(terms, ind2, invfile)
        docs = getCommonDocs(lookup)
        rank = doc_score(lookup, docs, terms)

        results = 0
        for url in rank:
            if results == 10:
                break
            print("{:2d}".format(results+1), url_id[int(url[0])])
            results += 1

        while results < 10 and len(lookup) > 0:
            del lookup[0]
            docs2 = getCommonDocs(lookup)
            rank2 = doc_score(lookup, docs2, terms)
            for url in rank2:
                if results == 10:
                    break
                if url[0] in [x for x,_ in rank]:
                    continue
                print("{:2d}".format(results+1), url_id[int(url[0])])
                results += 1
            rank = rank + rank2
        if results == 0:
            print("no results.")
        print("search time: " + str(time.time() - start) + " seconds\n")
    invfile.close()


def indexLookup(terms, ind2, invfile):
    lookup = []
    for word, num in terms.items():
        if word[0] in ind2:
            invfile.seek(ind2[word[0]])
        for n, line in enumerate(invfile):
            if n % 2 == 0:
                if line.rstrip('\n') == word:
                    idf = invfile.readline().rstrip(";\n")
                    tdict = dict()
                    length = 0
                    for doc in idf.split(";"):
                        urlid, fq, im = doc.split(",")
                        tdict[urlid] = [fq, im]
                        length += 1
                    lookup.append([word, length, tdict])
                    break
            if line[0] > word[0]:
                break
    return sorted(lookup, key=lambda x: x[1])


def getCommonDocs(lookup):
    common = set()
    for word, length, invdoc in lookup:
        if common == set():
            for key in invdoc.keys():
                common.add(key)
        else:
            temp = set()
            for doc in common:
                if doc in invdoc:
                    temp.add(doc)
            common = temp
    return common


def doc_score(lookup, docs, terms):
    ranking = []
    for doc in docs:
        total = 0
        for word, df, tdict in lookup:
            if doc not in tdict:
                continue
            tf, im = tdict[doc]
            total += tfidf(tf, df, im) * (10 + int(terms[word]))/10
        ranking.append([doc, total])
    return sorted(ranking, key=lambda t: -t[1])


def tfidf(tf, df, im, N=40327):
    return (int(im)/5 + 1 + math.log10(int(tf))) * math.log10(int(N)/int(df))


if __name__ == "__main__":
    startSearch()
