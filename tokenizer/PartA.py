import re
import sys


# time complexity of this function is O(length of file)
def tokenize(filepath):
    tokens = []
    with open(filepath) as infile:
        # for loop runs in O(n) where n is number of lines in file
        for line in infile:
            # re.findall runs in O(m) where the line has a length of m
            tokens += re.findall('[A-Za-z0-9]+', line)

    # Take the lowercase alphanumeric token from list and adds it to a set which removes duplicates
    # This runs in O(n) time as it has to loop through the list and add it into the set
    return set(x.lower() for x in tokens)


# time complexity of this function is O(length of file)
def computeWordFrequencies(filepath, tokens):
    # creates dict of keys of the tokens, so O(k) where k is len of tokens
    word_map = dict.fromkeys(tokens, 0)
    with open(filepath) as infile:
        # nested for loop so runs in O(n*m),
        # where n is number of lines and m is number of tokens per line
        for line in infile:
            # re.findall runs in O(m) and then the for loop goes through the list which is O(m) again
            for each in re.findall('[A-Za-z0-9]+', line):
                word_map[each.lower()] += 1
    return word_map


# Time complexity of this function is O(nlogn)
def freq_print(word_map):
    # O(n) to loop through each key,value in the word_map dictionary and O(nlogn) to sort the dictionary
    # so the total time complexity is O(nlogn)
    for key, value in sorted(word_map.items(), key=lambda t: -t[1]):
        print(key + ' = ' + str(value))


if __name__ == '__main__':
    try:
        # checks if any extra arguments were given
        if len(sys.argv) > 2:
            raise IndexError
        freq_print(computeWordFrequencies(sys.argv[1], tokenize(sys.argv[1])))
    except FileNotFoundError:
        print("FileNotFoundError: File argument does not exist.")
    except IndexError:
        print("IndexError: Incorrect number of command line arguments.")

