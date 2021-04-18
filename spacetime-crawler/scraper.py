import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from collections import defaultdict
import pickle
import hashlib


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    if resp.status >= 400 or resp.status < 200:
        return []

    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    except AttributeError:
        return []

    # ignore if not enough content on webpage
    if len(soup.get_text()) < 200:
        return []

    try:
        word_freq = pickle.load(open("word_freq.p", "rb"))  # keeps track of most frequent words
        sites = pickle.load(open("sites.p", "rb"))  # keeps track of sites visited and number of words on page
        hashes = pickle.load(open("hashes.p", "rb"))  # keeps track of fingerprints of every page visited for simhash
    except FileNotFoundError:
        word_freq = defaultdict(int)
        sites = defaultdict(int)
        hashes = set()

    # simhash implementation
    content = soup.get_text()
    fingerprint = simhash(content)
    for fp in hashes:
        if comparison(fingerprint, fp) > 0.90:
            return []
    hashes.add(fingerprint)

    for each in re.findall('[A-Za-z0-9]+', content):
        word_freq[each.lower()] += 1
        sites[url] += 1

    # ignore if not enough content on webpage
    if sites[url] < 100:
        return []

    pickle.dump(word_freq, open("word_freq.p", "wb"))
    pickle.dump(sites, open("sites.p", "wb"))
    pickle.dump(hashes, open("hashes.p", "wb"))

    links = set()  # use a set to remove duplicates
    for tag in soup.find_all('a'):
        link = tag.get('href')
        try:
            parse = urlparse(link)
            query_blacklist = re.compile(".*(share=|replytocom=|ical=|comment).*")
            if query_blacklist.search(parse.query):
                link = link.split('?')[0]  # remove query if contains blacklisted words
            if parse.fragment is not "":
                link = link.split('#')[0]  # remove fragment if present
            if parse.netloc == "" and link != "":
                if url[-1] != "/" and "." not in urlparse(url).path:  #only add a slash if no period in path
                    link = urljoin(url + "/", link)
                else:
                    link = urljoin(url, link)
            if link is not None and link != "":
                links.add(link)
        except (AttributeError, TypeError):
            pass

    return list(links)  # change set back to list


def is_valid(url):
    if url is None or url == "":
        return False

    try:
        sites = pickle.load(open("sites.p", "rb"))
    except FileNotFoundError:
        sites = defaultdict(int)
    if url in sites:
        return False

    if re.match(r".*\/(css|js|bmp|gif|jpe?g|ico"
                  + r"|png|tiff?|mid|mp2|mp3|mp4|odp"
                  + r"|wav|avi|mov|mpe?g|ram|m4v|mkv|ogg|ogv|pdf|pdfs"
                  + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                  + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                  + r"|epub|dll|cnf|tgz|sha1|apk|ova|war|mat"
                  + r"|thmx|mso|arff|rtf|jar|csv|pps|ppsx|sit"
                  + r"|rm|smil|wmv|swf|wma|zip|rar|gz)($|\/.*)", url.lower()):
        return False

    try:
        parsed = urlparse(url)

        # check if url is within the allowed domains
        domain = re.compile(".*(\.stat\.uci\.edu\/|\.ics\.uci\.edu\/|\.cs\.uci\.edu\/|\.informatics\.uci\.edu\/|today\.uci\.edu\/department\/information_computer_sciences\/).*")
        if not domain.search(url):
            return False

        # added "apk, ova, war, mat, pps, ppsx, sit, odp" in addition to initial extensions
        if re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4|odp"
                + r"|wav|avi|mov|mpe?g|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1|apk|ova|war|mat"
                + r"|thmx|mso|arff|rtf|jar|csv|pps|ppsx|sit"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", url.lower()):
            return False

        return True

    except TypeError:
        print("TypeError for ", parsed)
        raise


def simhash(text):
    wordmap = hashedWordFreq(text)
    fp = [0] * 160
    for binary, num in wordmap.items():
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


def hashedWordFreq(text):
    # creates dict of words and their frequencies, then hashes the results to be used with simhash
    word_map = defaultdict(int)
    for each in re.findall('[A-Za-z0-9]+', text):
        word_map[each.lower()] += 1
    hashedmap = defaultdict(int)
    for key, value in word_map.items():
        hashedmap[hex2bin(hashlib.sha1(key.encode()).hexdigest())] = value
    return hashedmap


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
