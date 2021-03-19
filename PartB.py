from PartA import tokenize
import sys


# time complexity of function is O(length of larger file)
def intersectionTokens(file1, file2):
    # tokenize function runs in O(m) where m is length of file
    # O(m) + O(m) is time complexity of O(m)
    tokens1 = tokenize(file1)
    tokens2 = tokenize(file2)

    # finding the intersection between the two sets is O(n)
    return len(tokens1.intersection(tokens2))


if __name__ == "__main__":
    try:
        # checks if the correct number of arguments were given
        if len(sys.argv) > 3 or len(sys.argv) < 2:
            raise IndexError
        print(intersectionTokens(sys.argv[1], sys.argv[2]))

    except FileNotFoundError:
        print("FileNotFoundError: File argument does not exist.")
    except IndexError:
        print("IndexError: Incorrect number of command line arguments.")
