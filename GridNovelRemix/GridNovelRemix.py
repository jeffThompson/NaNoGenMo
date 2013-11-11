
'''
GRID NOVEL REMIX
Jeff Thompson | 2013 | www.jeffreythompson.org

Crawl through and remix a novel. Created for #NaNoGenMo.

An existing text is loaded word-by-word, then organized 
into a 2D grid. Using a random start position in the grid, 
the "cursor" is moved up, down, left, or right and that 
word is added. The process is repeated up to 50k words. 

Random commas, periods, and paragraph breaks are also 
added along the way.

Most of the code: fixing weird glitches via a LOT of regex.

TO TRY OR CONSIDER:
+ when word is selected, it is removed (replaced with ''), or skip over to next above, etc
+ step not just in increments of 1 (1 up/down but further left/right)

TO DO:
+ 

This project is released under a Creative Commons BY-NC-SA
License - feel free to use, but please let me know.

'''

import os, re, math, random

input_filename = 'LOTR_Poem.txt'
#input_filename = 'LordOfTheRings.txt'
#input_filename = 'TaleOfTwoCities.txt'
#input_filename = 'WarOfWorlds.txt'

capitalize_characters = False
characters = [ 'frodo', 'baggins', 'sam', 'samwise', 'gamgee', 'merry', 'brandybuck', 'peregrin', 'pip', 'pippin', 'gandalf', 'aragorn', 'legolas', 'gimli', 'denethor', 'boromir', 'faramir', 'galadriel', 'celeborn', 'elrond', 'arwen', 'bilbo', 'theoden', 'eomer', 'eowyn', 'treebeard', 'sauron', 'nazgul', 'saruman', 'grima', 'wormtongue', 'gollum', 'smeagol', 'shelob', 'balrog' ]

word_count = 77
allow_repeat = False
all_lowercase = True
replace_a_an = True
numbers_as_words = True		# replace 0-19 as text representation

chance_newline = 0.01
chance_comma = 0.03
chance_period = 0.1
chance_question = 0.001

add_dialog_quotes = True
pronouns = '(he|she|it)'
pronouns_upper = '(He|She|It)'
said = '(said|whispered|yelled|commanded|urged|plead|muttered)'
asked = '(asked|queried|inquired|demanded|begged)'

add_random_chapters = True
chance_chapter = 0.02
chapter_equals_new_location = False

add_end_text = True

# not really all articles, but basically words we don't want to end a sentence with
articles = [ 'a', 'an', 'the', 'and', 'or', 'if', 'of', 'by', 'as' ]

# words to capitalize - list in lowercase! (could include names, places, etc)
words_to_capitalize = [ 'i' ]

# list of punctuation marks to look for
punctuation = [ '.', ',', '?', '!' ]

# output files
output_filename = 'Output/' + os.path.splitext(input_filename)[0] + '_AllowRepeat-' + str(allow_repeat) + '_AllLowercase-' + str(all_lowercase) + '_' + str(word_count) + 'Words.txt'
step_filename = 'StepFiles/' + os.path.splitext(input_filename)[0] + '_AllowRepeat-' + str(allow_repeat) + '_AllLowercase-' + str(all_lowercase) + '_' + str(word_count) + 'Words.txt'
words_filename = 'WordLists/' + os.path.splitext(input_filename)[0] + '_WordList.txt'

# other variables (set later)
words = []
book = ''
steps = ''
capitalize = True
in_dialog = False
chapter = 1

# os.system('cls' if os.name=='nt' else 'clear')
print ('\n' * 4)

# create a divider between listings based on size of Terminal window
columns = 40
rows, columns = os.popen('stty size', 'r').read().split()
display_divider = '- ' * (int(columns)/2)

# extract words
with open('SourceFiles/' + input_filename) as file:
	for line in file:
		line = re.sub(r'-', ' ', line)							# change dash to space (avoids some smashed word issues)
		for word in line.split(' '):
			word = re.sub(r'[^\'\w]', '', word)				# strip whitespace but leave apostrophes
			# word = re.sub(r'\W', '', word)					# former version, works for everything but kills apostrophes
			word = re.sub(r'_', '', word)							# get rid of random _
			if word.isupper() or all_lowercase:				# if all uppercase, set to lower case instead
				word = word.lower()
			if word.lower() in words_to_capitalize:		# if capitalize flag set, set to title case
				word = word.title()
			words.append(word)
		
		# OPTIONAL VERSION: 
		# get all words using NLTK - seems to add some weirdness, so probably not the best choice...
		# requires this import statement: from nltk.tokenize import RegexpTokenizer
		'''
		tokenizer = RegexpTokenizer('\w+')
		for word in tokenizer.tokenize(line):
			word = re.sub(r'_?!.', '', word)					# replace random leftovers
			if word.isupper() or all_lowercase:				# if all uppercase, set to lower case instead
				word = word.lower()
			if word.lower() in words_to_capitalize:		# if capitalize flag set, set to title case
				word = word.title()
			words.append(word)
		'''

# get grid size, set random start point
width = int(math.sqrt(len(words)))
height = len(words) / width
for i in range((width*height) - len(words)):
	words.append('')
x = random.randrange(0, width)
y = random.randrange(0, height)
pos = (y * width) + x

# add size and starting data to file
steps = str(width) + ',' + str(height) + ',' + str(pos)

# title and metadata
title = 'Grid Remix: ' + re.sub(r'([a-z])([A-Z])', r'\1 \2', input_filename)
title = re.sub(r'\.txt', '', title)
book += title.upper() + '\n' + 'An algorithmic novel by Jeff Thompson, created for National Novel Generation Month 2013'

metadata = 'Word count = ' + str(word_count)
metadata += ', allow word repetition = ' + str(allow_repeat).lower() + ', chance of a new chapter = ' + str(chance_chapter * 100)
metadata += '%, chance of new paragraph = ' + str(chance_newline * 100) + '%, chance of a comma = ' + str(chance_comma * 100)
metadata += '%, chance of a period = ' + str(chance_period * 100) + '%, chance of question mark = ' + str(chance_question * 100) + '%'
book += '\n\n' + metadata + '\n\n\n'

chance_comma = 0.03
chance_period = 0.1
chance_question = 0.001
chance_chapter = 0.02

# iterate and create text!
if add_random_chapters:
	book += 'CHAPTER ' + str(chapter)
	book += ' (' + str(pos % width) + ', ' + str(pos / width) + ')'
	book += '\n\n'

for step in range(word_count):
	# move in random direction (U R D L)
	if allow_repeat:
		dir = random.randrange(0,5)			# '5' won't do anything, just stay in place :)
	else:
		dir = random.randrange(0,4)
	
	# save steps (lets us draw it out later)
	steps += str(dir) + '\n'
	
	# up
	if dir == 0:
		pos -= width
	
	# right
	elif dir == 1:
		pos += 1
	
	# down
	elif dir == 2:
		pos += width
	
	# left
	elif dir == 3:
		pos -= 1
	
	# if past the edge of the grid, wrap
	if pos < 0:
		pos += word_count
	elif pos >= word_count:
		pos %= word_count
	
	# add word to book
	word = words[pos]
	if capitalize:
		word = word.title()
		capitalize = False
	book += word

	# random punctuation
	if random.random() < chance_comma:
		book += ','
	elif random.random() < chance_period and word.lower() not in articles:
		book += '.'
		capitalize = True			
	elif random.random() < chance_question and word.lower() not in articles:
		book += '?'
		capitalize = True

	# random new paragraph and chapter
	if random.random() < chance_newline and word.lower() not in articles:
		book += '.\n\n'													# be sure to add a period first
		if random.random() < chance_chapter:		# random chapter
			chapter += 1
			book += '\nCHAPTER ' + str(chapter) 
			if chapter_equals_new_location:
				book += ' (' + str(pos % width) + ', ' + str(pos / width) + ')'
				pos = random.randrange(0, len(words))
			book += '\n\n'				
		capitalize = True
	elif step < (word_count-1):		# no space at end of book (makes the period look weird)
		book += ' '

# add a period at the end
if book[:-2] not in punctuation:
	book += '.'

# clean up any weirdness (easier than fixing in the code above... a hack, I know)
book = re.sub(r',+\.+', '.', book)						# , followed by .
book = re.sub(r'\?+\.+', '?', book)						# ? followed by .

book = re.sub(r'\s+\.+', '.', book)						# space before .
book = re.sub(r'\s+,+', ',', book)						# space before ,

book = re.sub(r',{2,}', ',', book)						# more than 1 ,
book = re.sub(r'\.{2,}', '.', book)						# ditto .
book = re.sub(r'[^\S\r\n]{2,}', ' ', book)		# 2 or more spaces (ignore \n and \r)

# LOTR causes major problems; this may be the lesser of many evils...
book = re.sub(r'[^a-zA-Z]\'+', ' ', book)			# remove ' at start of word
book = re.sub(r'\'[^a-zA-Z]', ' ', book)			# ditto end of word

# wow, super ugly: remove extra space at the start of paragraphs and capitalize as needed
book = re.sub(r'\n.*?(\b[a-zA-Z])', lambda pat: '\n' + pat.group(1).upper(), book)

# also ugly: make sure all sentences are capitalized (may be wrong after some of the regex above...)
book = re.sub(r'(\.|\?) ([a-z])', lambda pat: pat.group(1) + ' ' + pat.group(2).upper(), book)

# capitalize any characters listed - forms regex as (name|name|name|name)
if capitalize_characters:
	book = re.sub(r'\bi(\b|\')', 'I\1', book)														# capitalize 'i'
	char_regex = '(' + '|'.join(char for char in characters) + ')'			# format regex
	book = re.sub(char_regex, lambda pat: pat.group(1).title(), book)		# replace!

# fix oddly capitalized letters after apostrophes (catches instances of things like he'Ll too)
book = re.sub(r'\'([A-Z].*?)\b', lambda pat: '\'' + pat.group(1).lower(), book)

# replace a/an mismatches (if specified)
if replace_a_an:
	book = re.sub(r'\b(A|a)\b ([aeiouAEIOU])', r'\1n \2', book)
	book = re.sub(r'\b(An|an)\b ([^aeiouAEIOU])', lambda pat: pat.group(1)[0] + ' ' + pat.group(2), book)

# fix any missing end-of-paragraph periods
book = re.sub(r'(\b[^\.]\n+)', r'.\1', book)

# add quotes around what seems like dialog
if add_dialog_quotes:
	book = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + said + '\.', r'.\n\n"\1," \2 \3.\n\n', book)
	book = re.sub(r'\.\W' + pronouns_upper+ ' ' + said + ' ([^\.]*?)\.', r'.\n\n\1 \2, "\3."\n\n', book)

	book = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + asked + '\.', r'.\n\n"\1?" \2 \3.\n\n', book)
	book = re.sub(r'\.\W' + pronouns_upper + ' ' + asked + ' ([^\.]*?)\.', r'.\n\n\1 \2, "\3?"\n\n', book)

	book = re.sub(r'"(\b[a-z])', lambda pat: '"' + pat.group(1).upper(), book)

# replace 0-19 with word representation, don't change for chapter #s
if numbers_as_words:
	book += re.sub(r'(?<!(chapter)) \b(1)\b', r' one', book)
	book += re.sub(r'(?<!(chapter)) \b(2)\b', r' two', book)
	book += re.sub(r'(?<!(chapter)) \b(3)\b', r' three', book)
	book += re.sub(r'(?<!(chapter)) \b(4)\b', r' four', book)
	book += re.sub(r'(?<!(chapter)) \b(5)\b', r' five', book)
	book += re.sub(r'(?<!(chapter)) \b(6)\b', r' six', book)
	book += re.sub(r'(?<!(chapter)) \b(7)\b', r' seven', book)
	book += re.sub(r'(?<!(chapter)) \b(8)\b', r' eight', book)
	book += re.sub(r'(?<!(chapter)) \b(9)\b', r' nine', book)
	book += re.sub(r'(?<!(chapter)) \b(10)\b', r' ten', book)
	book += re.sub(r'(?<!(chapter)) \b(11)\b', r' eleven', book)
	book += re.sub(r'(?<!(chapter)) \b(12)\b', r' twelve', book)
	book += re.sub(r'(?<!(chapter)) \b(13)\b', r' thirteen', book)
	book += re.sub(r'(?<!(chapter)) \b(14)\b', r' fourteen', book)
	book += re.sub(r'(?<!(chapter)) \b(15)\b', r' fifteen', book)
	book += re.sub(r'(?<!(chapter)) \b(16)\b', r' sixteen', book)
	book += re.sub(r'(?<!(chapter)) \b(17)\b', r' seventeen', book)
	book += re.sub(r'(?<!(chapter)) \b(18)\b', r' eighteen', book)
	book += re.sub(r'(?<!(chapter)) \b(19)\b', r' nineteen', book)

# if specified, add 'END' to book
if add_end_text:
	book += '\n\n\n' + 'END'

# print results and save
print book
with open(output_filename, 'a') as file:
	file.write(book)
with open(step_filename, 'a') as file:
	file.write(steps)
with open(words_filename, 'a') as file:
	for word in words:
		file.write(word + '\n')

# done!
print '\n' + display_divider + '\n'
print 'word count:       ' + ('{:,}'.format(len(words)))
print 'grid dimensions:  ' + str(width) + ' x ' + str(height)
print 'start coords:     ' + str(x) + ' x ' + str(y)
print 'chapters created: ' + str(chapter)
print '\n\nDONE!'
print ('\n' * 8)
