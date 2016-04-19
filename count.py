import os
import glob
import re

all_lines = [] # we define a list called all_lines
rhyme_words = set() # we define a tuple called 'rhyme words'

### CLEANING THE DATA ###
for filename in glob.glob("rijm/*.xml"):
	print(filename)
	lines = open(filename, 'r').readlines() # open filename with mode 'read'
	lines = [line.strip() for line in lines if line.strip().startswith("<l>")]
	for line in lines:
		line = line.replace("<l>", "").replace("</l>", "") # <l> at the beginning and </l> at the end of a verse line will be deleted
		if "<gap/>" in line or "..." in line: # <gap/> and ... occur frequently in verse lines. These are not words, so they must be deleted
			print(line) # all lines with <gap/> or ... will be printed
			continue
		line = re.sub('<[^>]*>', '', line).lower() # this regex removes the entire xml-code that comes before the actual verse lines (i.e. all secondary information that comes with a text will be deleted)
		line = "".join([char for char in line if char.isalpha() or char.isspace()]) # what does this line mean?

### DEFINE WHAT ARE RHYME WORDS ###		
		words = line.split() # each line is split into seperate words using a space as delimiter. Every line is now split up into words.
		if words:
			rhyme = words[-1] # we define a rhyme as the final word of a line
			rhyme_words.add(rhyme) # rhyme words are added to the tuple called 'rhyme_words'
			all_lines.append(words) # we add all the words to the list called 'all_lines'

F = open("out_of_vocabulary.txt", "w+") # the file out_of_vocabulary.txt is opened ('w+' stands for read/write mode, if the file already exists override it (empty it)
fully_covered = 0 # initialize the value of fully_covered to 0
for line in all_lines:
	covered = False
	for w in line[:-1]: # ignore original rhyme word
		if w in rhyme_words: # what is 'w'?
			covered = True	
		else:
			covered = False
			F.write(" ".join(line)+' > '+w+"\n")
			break
	if covered:
		fully_covered+=1
F.close()
print(len(all_lines))
print(len(rhyme_words))
with open("unique_rhyme_words.txt", "w+") as F:
	F.write("\n".join(sorted(list(rhyme_words))))
print(fully_covered)
print(fully_covered/float(len(all_lines)))