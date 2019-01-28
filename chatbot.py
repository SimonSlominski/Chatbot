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


# 1.8 Creating a dict that maps each word to its number of occurences
word2count = {}

for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1

for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1


# 1.9 Filtering non frequent words by creating two dictionaries that 
# map the questions words and the answers words to a unique integer
treshold = 20

questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= treshold:
        questionswords2int[word] = word_number
        word_number += 1

answerswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= treshold:
        answerswords2int[word] = word_number
        word_number += 1

# return: two identical dictionaries


# 1.10 Tokenization: adding the last tokens to these two dictionaries
""" 
Tokens are usefull to encoder and decoder with seq2seq model. 
SOS - start of string
EOS - end of string
OUT - token == trashold. In this case is 5% of non frequent words
"""
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

for token in tokens:
    questionswords2int[token] = len(questionswords2int) +1

for token in tokens:
    answerswords2int[token] = len(answerswords2int) +1
    

# 1.11 Creating the inverse dictionary of the answerswords2int dictionary
# w == word; i == int; w_i - values in dict, w - keys in dict
# nice trick to inverse dict!
answersints2word = {w_i: w for w, w_i in answerswords2int.items()}


# 1.12 Adding the 'End of string' token to the end of every answer
# Remember to add 'space' between last word in line and '<EOS>' token
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'


# 1.13 Translating all the questions and the answers into integers
# and replacing all the words that were filtered out by <OUT>
questions_into_int = []

for question in clean_questions:
    ints= []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_into_int.append(ints)

answers_into_int = []

for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)


# 1.14 Sorting questions and answers by the length of questions
sorted_clean_questions = []
sorted_clean_answers = []

for length in range(1, 25+1):
    for i in enumerate(questions_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_into_int[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])

"""
Use enumerate() with a tuple instead of a list, 
this way you can give more meaningful names to the loop variables

for i, question_int in enumerate(questions_int):
        if len(question_int) == length:
            sorted_clean_questions.append(questions_int[i])
            sorted_clean_answers.append(answers_int[i])
"""

