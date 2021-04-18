import json
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from nltk.stem import PorterStemmer
import time
import hashlib


def inverse_index():
    url_id = []
    inv_index = dict()
    ps = PorterStemmer()
    txtcount = 1
    count = 0
    hashes = set()
    for path, directories, files in os.walk("DEV"):
        for json_file in files:
            if ".json" in json_file:
                with open(os.path.join(path, json_file)) as jfile:
                    d = json.load(jfile)
                    print(count, json_file, d['url'])
                    soup = BeautifulSoup(d['content'], 'html.parser')
                    d['url'] = d['url'].split('#')[0]  # defragment the url
                    if d['url'] in url_id:
                        continue

                    content = soup.get_text(separator=' ')
                    word_map = defaultdict(int)
                    for each in re.findall('[A-Za-z0-9]+', content):
                        word_map[ps.stem(each.lower())] += 1
                    fingerprint = simhash(word_map)  # check if url is a duplicate or near duplicate of another url
                    dup = False
                    for fp in hashes:
                        if comparison(fingerprint, fp) > 0.95:
                            dup = True
                    if dup:
                        continue
                    hashes.add(fingerprint)
                    url_id.append(d['url'])

                    for word, freq in word_map.items():
                        if word not in inv_index:
                            inv_index[word] = dict()
                        if count not in inv_index[word]:
                            inv_index[word][count] = [0, 0]  # first element is frequency, second is importance of word
                        inv_index[word][count][0] += freq

                    # update the inverted index with important text
                    inv_index = important_title(soup, ps, inv_index, count)
                    inv_index = important_text(soup, ps, inv_index, count, ['h1', 'h2', 'h3'], 2)
                    inv_index = important_text(soup, ps, inv_index, count, ['strong', 'b'], 1)
                    count += 1

                # offload inverted index when number of documents reached
                if count % 7000 == 0:
                    offload_index(inv_index, txtcount)
                    inv_index = dict()
                    txtcount += 1

    if len(inv_index) > 0:
        offload_index(inv_index, txtcount)
        txtcount += 1

    with open("url_index.txt", "w") as urlfile:
        urlfile.write(str(url_id))
    merge_indexes(txtcount-1)


def important_title(soup, ps, inv_index, count):
    if soup.title is not None:
        for title in re.findall('[A-Za-z0-9]+', soup.title.get_text()):
            title = ps.stem(title.lower())
            if title not in inv_index:
                inv_index[title] = dict()
            if count not in inv_index[title]:
                inv_index[title][count] = [1, 0]
            inv_index[title][count][1] = 3
    return inv_index


def important_text(soup, ps, inv_index, count, types, value):
    for head in soup.find_all(types):
        if head is None:
            continue
        for word in re.findall('[A-Za-z0-9]+', head.get_text()):
            word = ps.stem(word.lower())
            if word not in inv_index:
                inv_index[word] = dict()
            if count not in inv_index[word]:
                inv_index[word][count] = [1, 0]
            inv_index[word][count][1] = max(value, inv_index[word][count][1])
    return inv_index


def offload_index(inv_index, txtcount):
    """Offloads current inverted index to a text file to be merged later"""
    starttime = time.time()
    with open("partial" + str(txtcount) + ".txt", "w") as txtfile:
        for key, value in sorted(inv_index.items()):
            txtfile.write('%s;%s\n' % (key, str(value)))
    print("offload time: " + str(time.time() - starttime))


def merge_indexes(num):
    """merge all partial indexes into one final inverted index"""
    start = time.time()
    files = []
    final = open("finalindex.txt", "w")
    abc = dict()  # byte positions of each letter in final inverted index
    alphabet = "02468abcdefghijklmnopqrstuvwxyz~"  # alphabet for comparison
    for n in range(num):
        files.append(open("partial" + str(n+1) + ".txt", "r"))

    compare = dict()
    for i, ea in enumerate(files):
        line = ea.readline().strip().split(";")
        if line[0] not in compare:
            compare[line[0]] = [[i], eval(line[1])]
        else:
            compare[line[0]][0].append(i)
            compare[line[0]][1].update(eval(line[1]))

    counter = 0
    while len(compare) > 0:
        word, (fl, df) = sorted(compare.items(), key=lambda t: t[0])[0]
        if word[0] == alphabet[0]:
            abc[alphabet[0]] = final.tell()
            alphabet = alphabet[1:]
        txt = word + "\n"
        for k2, v2 in sorted(df.items()):
            txt += str(k2) + "," + str(v2[0]) + "," + str(v2[1]) + ";"
        final.write(txt[:-1] + "\n")
        del compare[word]
        for n in fl:
            fileline = files[n].readline().strip().split(";")
            if fileline == [""]:
                continue
            wd, idf = fileline
            if wd not in compare:
                compare[wd] = [[n], eval(idf)]
            else:
                compare[wd][0].append(n)
                compare[wd][1].update(eval(idf))
        counter += 1

    for f in files:
        f.close()
    final.close()
    with open("indexindex.txt", "w") as indx:
        indx.write(str(abc))
    print("merging total time: " + str(time.time() - start))
    print("count " + str(counter))


def simhash(word_map):
    hashedmap = defaultdict(int)
    for key, value in word_map.items():
        hashedmap[hex2bin(hashlib.sha1(key.encode()).hexdigest())] = value
    fp = [0] * 160
    for binary, num in hashedmap.items():
        for i, digit in enumerate(binary):
            if digit == "0":
                fp[i] += num
            else:
                fp[i] -= num
    hashed = ""
    for x in fp:
        if int(x) > 0:
            hashed += "1"
        else:
            hashed += "0"
    return hashed


def hex2bin(num):
    # hexadecimal to binary
    conversion = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101",
                  "6": "0110", "7": "0111", "8": "1000", "9": "1001", "a": "1010", "b": "1011",
                  "c": "1100", "d": "1101", "e": "1110", "f": "1111"}
    binary = ""
    for i in num:
        binary += conversion[i]
    return binary


def comparison(hash1, hash2):
    # comparison between two hash numbers for simhash
    count = 0
    for i in range(0,len(hash1)):
        if hash1[i] == hash2[i]:
            count += 1
    return count / len(hash1)


if __name__ == "__main__":
    inverse_index()


