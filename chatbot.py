# Importing the libraries
import numpy as np
import tensorflow as tf
import time
import re


# Part 1 - Data Preprocessing

# 1.1 Importing the dataset
# Check if you are in your working directory (pwd in Spider's console)
lines = open('movie_lines.txt', encoding = 'UTF-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'UTF-8', errors = 'ignore').read().split('\n')


# 1.2 Create dictionary to map each line and its ID
id2line = {}

for line in lines:
    _line = line.split(' +++$+++ ')
    # Check if, in fact, the _line variable contains 5 elements
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
        
        
# 1.3 Create a list of all of the conversations
conversations_ids = []

for conversation in conversations[:-1]:
    # Take last element from the list and remove square brackets, quotes
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))
    
    
# 1.4 Getting separately the questions and the answers
questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
    

# 1.5 Cleaning the texts
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

# 1.6 Cleaning the questions
clean_questions = []

for question in questions:
    clean_questions.append(clean_text(question))    

# 1.7 Cleaning the answers
clean_answers = []

for answer in answers:
    clean_answers.append(clean_text(answer))











































