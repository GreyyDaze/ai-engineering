"""
Task:
- Accepts a .txt file path as a command-line argument,
- reads the file  and clean it ,
- splits it into sentences,
- counts word frequency,
- prints the 10 most common words and the total sentence count.
- Handle missing file paths and empty files gracefully with informative error messages.
"""

# issue fix
# use different names for variable for the following reasons
    # 1. for clarity and avoiding confusion 
    # 2. and name base on what steps you are on to avoid the naming colloision
# Use split() not split(" "), to remove all the whitespace in b/w

# self-reflections
# What I faced:
# → Not knowing what to clean until I saw the data
# → Not knowing whether to mutate or create new variables

# What I learned:
# → Handle the common cases first. Add edge cases 
#   when production tells you what breaks.
# → If the data is needed later, don't modify it directly. 
#   If it's not reused, save yourself the extra variable.

# Both are production decisions, not Python decisions.

"""
Solution
"""

# step 1 -> accepts a file path
# provide argument docs, and has built in error handling
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Path of your file")
args = parser.parse_args()
file_path = args.file
print(f"\n Received file path: {file_path} and type is {type(file_path)} \n")

# step 2 -> read the file 
try: 
    with open(file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
        print(f"Raw text from the file are: {raw_text} \n")
        if raw_text == "":
            print("File is empty, cant be processed further. \n")
            sys.exit()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. \n")
    sys.exit()

# step 3 -> split it into sentences.
sentence_list = raw_text.split(".")

print(f"List of separate sentences: {sentence_list} \n")

# step 4 -> clean up the list of lines
cleaned_list = []
# remove white space from each string
for line in sentence_list:
    cleaned_list.append(line.strip())

# remove empty strings
cleaned_list = list(filter(None, cleaned_list))    

print(f"Cleaned list with no whitespace and empty strings: {cleaned_list} \n")

# step 5a - count number of total sentence
# simple case
# total_sentences = len(cleaned_list)

# a little more efficient case
total_sentences = 0
for item in cleaned_list:
    words_count_per_sentence = len(item.split())

    if words_count_per_sentence > 1:
        total_sentences += 1

print(f"Number of total sentences in this file are: {total_sentences} \n")

# step 5b - count words frequency
# remove white space and dot
cleaned_lines = raw_text.replace("\n", "").replace(".", "")
print(f"Cleaned lines from the file are: {cleaned_lines} \n")

# lines into a word list
words_list = cleaned_lines.split(" ")
print(f"Word from the lines are: {words_list} \n")

# count word using loop and dictionary
words_count_file = {}
for word in words_list:
    if word not in words_count_file.keys():
        words_count_file[word] = 1
    else: 
        words_count_file[word] += 1

print(f"Word Count Dictionary: {words_count_file}")

# in descending order print the dictionary
sorted_word_by_count = dict(sorted(words_count_file.items(), key=lambda x:x[1], reverse=True))

print(f"Sorted Word Count Dictionary: {sorted_word_by_count} \n")

sorted_word_count_list = list(sorted_word_by_count.items())
print("Here are the ten most common words in the text file: \n")
for i in range(1, 11):
    word, count = sorted_word_count_list[i-1]
    if i==10:
        print(f"{i},  Word: {word}, Count: {count}")
    else: 
        print(f"{i},  Word: {word}, Count: {count}\n")
   
