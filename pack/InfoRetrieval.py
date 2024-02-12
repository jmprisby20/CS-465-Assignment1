# Jake Prisby, Abdel Rahman Albasha, and Nathaniel Burton
# CS 465 
# Winter 2024
# Project #1 

import nltk # Package for tokenization and normalization
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re # Regex package
import contractions 
import os

nltk.download('punkt') # Download tokenizer
nltk.download('stopwords') # Download stop words

# Desc.: Takes a string and performs tokenization and normalization
# Input: String of text
# Output: list of normalized words
# NOTE: This function is written following the tutorial found at: https://towardsdatascience.com/text-normalization-for-natural-language-processing-nlp-70a314bfa646
def process_string(str):
    # First expand contractions
    expanded = [] # Create List to store each word
    # Iterate over words in string
    for word in str.split():
        expanded.append(contractions.fix(word)) # Store expanded word in list
    expanded_str = " ".join(expanded) # Join list into string
    # Tokenize string
    tokenized_list = nltk.word_tokenize(expanded_str)
    # Remove punctuation
    filtered_list = [word for word in tokenized_list if word.isalpha()]
    # Remove stop words
    stop_words = set(stopwords.words('english')) # List of stop words
    filtered_list = [word for word in filtered_list if not word in stop_words]
    # Stemm words
    sb = SnowballStemmer('english')
    stemmed_list = [sb.stem(words_sent) for words_sent in filtered_list]
    return stemmed_list

def document_word_counter(doc_contents):
    word_count = {}
    for word in doc_contents:
        # Update counter for this 
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def soundex(word):
    soundex_dict = {'b': '1', 'f': '1', 'p': '1', 'v': '1',
                    'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
                    'd': '3', 't': '3',
                    'l': '4',
                    'm': '5', 'n': '5',
                    'r': '6'}
    # Convert word to uppercase and the first letter to the word's first letter
    word = word.lower()
    soundex_code = word[0]
    # Replace consonants with their respective Soundex values
    for char in word[1:]:
        if char in soundex_dict:
            code = soundex_dict[char]
            if code != soundex_code[-1]:
                soundex_code += code
    # Remove vowels and 'H', 'W' after the first letter
    soundex_code = soundex_code.replace('0', '')
    # Truncate or pad to make a four-character code
    soundex_code = soundex_code[:4].ljust(4, '0')
    return soundex_code.upper()

class InfoRetrieval:

    def __init__(self):
        self.inverted_index = {}
        self.word_counter = {}
        self.refresh_structures()

    def refresh_structures(self):
        # Reset the structures
        self.inverted_index = {}
        self.word_counter = {}
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the docs folder
        docs_dir = os.path.join(current_dir, '..', 'docs')
        for file_name in os.listdir(docs_dir):
            path = os.path.join(docs_dir, file_name)
            # Check if file exists
            if ( os.path.isfile(path) ):
                # Read file contents
                file_contents = open(path, encoding='utf-8').read()
                processed_contents = process_string(file_contents) # Perform normalization and tokenization
                # Update word counter
                self.word_counter[file_name] = document_word_counter(processed_contents)
                # Update inverted index
                processed_contents_no_dup = list(set(processed_contents))
                for word in processed_contents_no_dup:
                    if word in self.inverted_index:
                        self.inverted_index[word].append(file_name)
                    else:
                        self.inverted_index[word] = [file_name]
    
    def collection_total_word_count(self):
        count = 0
        for doc in self.word_counter:
            for word in self.word_counter[doc]:
                count+= self.word_counter[doc][word]
        return count
    
    def collection_unique_word_count(self):
        return len(self.inverted_index)

    def doc_total_word_count(self, doc_name):
        count = 0
        for word in self.word_counter[doc_name]:
            count+= self.word_counter[doc_name][word]
        return count

    def doc_unique_word_count(self, doc_name):
        return len(self.word_counter[doc_name])

    def binary_query(self, term1, term2, op):
        res = []
        try:
            # Convert inverted index entries for both words into sets
            set1 = set(self.inverted_index[term1])
            set2 = set(self.inverted_index[term2])
            # Perform set operations for query operation
            if op == 'and':
                res = set1.intersection(set2)
            else:
                res = set1.union(set2)
            res = list(res)
        except:
            pass
        return res
    
    