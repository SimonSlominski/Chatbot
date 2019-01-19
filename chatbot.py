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
    















