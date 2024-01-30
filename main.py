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

# Desc.: Takes a string and performs tokenizationa and normalization
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

# Desc.: Retrieves count for all words in the document
# Input: List of words
# Output: Dictionary of following format: { 'word': word_count, ... }
def update_word_count_for_doc(word_list):
    word_count = {}
    for word in word_list:
        # Update counter for this 
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# Desc.: Go through all files in doc folder and update word counter and inverse index
# NOTE: For some reason if I clear dictionary in this method it will remain clear even after completion
#       So instead perform the clear elsewhere to remove any words which are no longer present.
def refresh_counters():
    for file_name in os.listdir('docs'):
        path = os.path.join('docs', file_name)
        # Check file then process
        if os.path.isfile(path):
            # Update word counter
            file_contents = open(path, encoding='utf-8').read()
            word_list = process_string(file_contents)
            # Update Word counter
            doc_word_count[file_name] = update_word_count_for_doc(word_list)
            # Update Inverse Index

# Desc.: Get the number of times a given word occurs in a given document
# Output: Integer value of number occurence    
def num_count_of_word_in_doc(file_name, word):
    try:
        return doc_word_count[file_name][word]
    except:
        return 0

# Main Method
if __name__ == '__main__':
    reverse_index = {}

    # NOTE: The value below is a dictionary which will store the word counts for each document
    #       The key in the dictionary is the file name
    #       The value stored per key is a dictionary that stores the word count for every word in that document
    doc_word_count = {} 

    refresh_counters()
    
    a = num_count_of_word_in_doc('entertainment_1.txt', 'jakekek')
    print(a)
    

    