"""def count_char(line):
    return len(line)
input = input("Enter a word: ")

result = count_char(input)

print(f"The number of characters in the word is '{input} is:' {result}")"""

import time
import random

def generate_sentence(length=""):
    seed = int(time.time())
    words = ['Brian', 'peter', 'Come', 'Basketball', 'Walk', 'Run', 'This', 'him', 'have']
    spaces =[' ']
    characters = words + spaces
    random.seed(seed)
    sentence = ' '.join(random.choice(characters)for _ in range(length))
    return sentence
sentence_length = int(input("Enter the desired length: "))

generated_sentence = generate_sentence(sentence_length)
print(f"The generated sentence is: {generated_sentence}")

sentence_length = len(generated_sentence.split())
print(f"The generated sentence has: {sentence_length} letters")

word = generated_sentence
final = len(word)
print(f"The number of letters in the sentence is: {final} letters")

"""word = generated_sentence
final = len(word)

print(final)"""
