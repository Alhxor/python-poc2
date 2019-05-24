"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
codeskulptor.set_timeout(50)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    return [list1[ind] for ind in range(len(list1)) if list1[ind] not in list1[:ind]]

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
#    lst1, lst2 = list(list1), list(list2)
#    result = []
#    while len(lst1) != 0 and len(lst2) != 0:
#        if lst1[0] in lst2:
#            result.append(lst1.pop(0))
#        elif lst2[0] in lst2:
#            result.append(lst2.pop(0))
#    return result
    return [el1 for el1 in list1 for el2 in list2 if el1 == el2]

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    lst1, lst2 = list(list1), list(list2)
    result = []
    while len(lst1) != 0 and len(lst2) != 0:
        result.append(lst1.pop(0) if lst1[0] < lst2[0] else lst2.pop(0))        
    return result + lst1 + lst2 # one of them should be empty by now
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    half1, half2 = list1[:len(list1)/2], list1[len(list1)/2:]
    if half1[0] < half2[0]:
        left, right = half1, half2
    else:
        left, right = half2, half1
    return merge(merge_sort(left), merge_sort(right))


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    if len(word) == 1:
        return ['', word]
    first = word[0]
    rest_strings = gen_all_strings(word[1:])
    return [first] + [string[:ind] + first + string[ind:]
                      for string in rest_strings for ind in range(len(string) + 1)
                      if len(string) > 0] + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dfile = urllib2.urlopen(codeskulptor.file2url(filename))
    return [line[:-1] for line in dfile.readlines()]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()



