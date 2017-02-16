"""
Routes and views for the flask application.
"""
import string
from datetime import datetime
from flask import render_template, request, url_for
from FlaskWebProject import app

badchars = string.punctuation + string.digits
alphabets = string.ascii_lowercase

# Initialize a list that all corpus words will be stored in

corpus_list_raw = []

# Open and read a text file, then store the words in corpus_list

with open("big.txt", "r") as txtfile:
    for corpus_line in txtfile:
        corpus_line = corpus_line.lower().strip() # Change all alphabets to lower case, then remove leading and/or trailing whitespace(s)
        for char in corpus_line:
            if char in badchars: 
                if (char == chr(39)) and (("n"+char+"t") or (char+"s") in corpus_line): # Keep the punctuation on contraction words, e.g. "don't", "can't", "engineer's", etc.
                    continue
                else:
                    corpus_line = corpus_line.replace(char," ") # Remove digits and punctuation from all other words
        corpus_list_raw += corpus_line.split()

# Remove unwanted characters from corpus words that might still exist due to the addition of contraction words

corpus_list = [corpus_word.strip(badchars) for corpus_word in corpus_list_raw]



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
    )
	
@app.route('/check', methods=['POST'])
def check():
	"""Renders the addition sum page"""
	word=request.form['word']
	result=autocorrect(word)
	return render_template(
		'check.html',
		title='Spell Check',
		word=result,
	)

# Offer user the option to add input word to corpus
 
def addword(word):
    print("Would you like to add '{}' to the corpus? Enter 1 for YES, 0 for NO".format(word))
    while True:
        try:
            add_prompt = int(input(">>> "))
            if add_prompt == 1:
                corpus_list.append(word)
                print("New word successfully added!")
                break
            elif add_prompt == 0:
                print("Word not added")
                break
            else: # Prompts user again if an integer other than 1 or 0 is entered
                print("Wrong integer entered. Please try again")
        except ValueError: # Exception case stipulated to prevent error raised by entry of non-integer values
            print("Non-integer value entered. Please try again")
        
# Measure word distance(s) between input word and corpus word(s)

def worddistance(word, corpus_word):
    """Measures the difference between two words and returns an integer value as word distance"""
    
    global word_distance
    word_distance = 0
    
    # Compare input word and a word from the corpus, letter by letter
    
    if len(word) == len(corpus_word):
        for i in range(len(word)):
            if word[i] != corpus_word[i]:
                word_distance += 1
                
    # If corpus word is one letter shorter than input word, append a whitespace to the end of it to facilitate comparison
    
    elif len(word) - len(corpus_word) == 1:
        corpus_word_temp = corpus_word + " " 
        for i in range(len(word)):
            if word[i] != corpus_word_temp[i]:
                word_distance += 1
    
    return word_distance

def autocorrect(word):
    """Checks if input word is in corpus: if not, measures word distance and provides nearest word suggestions (if any)"""
    
    # Convert input word to lower case
    
    word = word.lower()
    
    # If input word contains unwanted character(s), print a reminder statement
    
    for char in badchars:
        if char in word and (char == word[0] or char == word[-1]): 
            return("Only alphabets allowed in word. Contraction words are exceptions. Try again.")
    
    # If input word is a single letter, print statement without calling worddistance()
    
    if (len(word) ==  1) and (word in alphabets): 
        return("The spelling is correct")
    
    # If input word is in corpus, print statement without calling worddistance()
    
    elif word in corpus_list:
        return("The spelling is correct")
    
    # In all other cases, invoke worddistance() to measure word differences
    
    else:
        # Initialize lists for storing suggested words later on
        
        suggested_words_initial = []
        suggested_words_temp = []
        
        for corpus_word in corpus_list:
            worddistance(word, corpus_word)
            if len(word) == 3: # If input word is of length 3, only return word suggestions that are of the same length or 1 letter less
                if word_distance == 1: 
                    suggested_words_initial.append(corpus_word)
            else:  # For all other cases, return word suggestions that are of word distance 1 or 2
                if (1 <= word_distance <= 2) and (len(word) == len(corpus_word)): 
                    suggested_words_initial.append(corpus_word) 
                elif (1 <= word_distance <= 2) and (len(word) - len(corpus_word) == 1):
                    suggested_words_initial.append(corpus_word)
                else:
                    continue
        
        # Convert list to set to remove duplicates, then convert back to list again
        
        suggested_words_temp = list(set(suggested_words_initial))
        
        # List comprehension used to generate and store tuples. A tuple consists of the frequency of suggested word in big.txt and the suggested word itself
        
        suggested_words = [(corpus_list.count(suggested_word), suggested_word) for suggested_word in suggested_words_temp]
        
        # The tuples above are stored with word frequency being in index 0 so that sorting could be performed. Most possible word(s) are listed in descending order
        
        suggested_words.sort(reverse = True)
        
        # Generate output depending on the length of word suggestion list
        
        if len(suggested_words) == 0:
            return("No suggestion available")
        
        else:
            return suggested_words[0][1]
            