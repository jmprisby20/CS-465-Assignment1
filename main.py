# Jake Prisby, Abdel Rahman Albasha, and Nathaniel Burton
# CS 465 
# Winter 2024
# Project #1 

import nltk # Package for tokenization and normalization
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re # Regex package
import contractions 

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
    filtered_list = [word for word in filtered_list if not word in stop_words]
    # Stemm words
    sb = SnowballStemmer('english')
    stemmed_list = [sb.stem(words_sent) for words_sent in filtered_list]
    return stemmed_list

# Main Method
if __name__ == '__main__':
    stop_words = set(stopwords.words('english')) # List of stop words
    # NOTE: This is just for testing
    s = open('docs\\food_1.txt').read()
    list = process_string(s)
    print(list)
    