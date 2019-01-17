# Importing the libraries
import numpy as np
import tensorflow as tf
import time
import re


# Part 1 - Data Preprocessing

# 1.1 Importing the dataset
lines = open('movie_lines.txt', encoding = 'UTF-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'UTF-8', errors = 'ignore').read().split('\n')
