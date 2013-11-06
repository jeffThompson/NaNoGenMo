
'''
GRID NOVEL REMIX
Jeff Thompson | 2013 | www.jeffreythompson.org

Crawl through and remix a novel. Created for #NaNoGenMo.

TO DO:
+ 
+ 
+ 

This project is released under a Creative Commons BY-NC-SA
License - feel free to use, but please let me know.

'''

import os, re, math, random

input_filename = 'LordOfTheRings.txt'
#input_filename = 'TaleOfTwoCities.txt'
chance_newline = 0.01
chance_comma = 0.03
chance_period = 0.05
word_count = 50000
no_repeat = False

output_filename = 'output/' + os.path.splitext(input_filename)[0] + '_AllowRepeat-' + str(no_repeat) + '_' + str(word_count) + 'Words.txt'
words = []
book = ''
capitalize = True

# os.system('cls' if os.name=='nt' else 'clear')
print '\n\n\n'

# extract words
print 'loading words...\n'
with open(input_filename) as file:
	for line in file:
		l = line.split(' ')
		for word in l:
			word = re.sub(r'\W', '', word)
			if word != '':
				words.append(word)

# get grid size
width = int(math.sqrt(len(words)))
height = len(words) / width
for i in range((width*height) - len(words)):
	words.append('')

x = random.randrange(0,width)
y = random.randrange(0,height)
pos = (y * width) + x
print 'word count:      ' + str(len(words))
print 'grid dimensions: ' + str(width) + ' x ' + str(height)
print 'start coords:    ' + str(x) + ' x ' + str(y)
print '\n- - - - - -\n'

# iterate!
for step in range(word_count):
	# move in random direction (U R D L)
	if no_repeat:
		dir = random.randrange(0,4)
	else:
		dir = random.randrange(0,5)		# won't do anything, just stay in place
	if dir == 0:
		pos -= width
	elif dir == 1:
		pos += 1
	elif dir == 2:
		pos += width
	elif dir == 3:
		pos -= 1
	
	# if past the edge of the grid, wrap
	if pos < 0:
		pos += word_count
	elif pos >= word_count:
		pos %= word_count
	
	# add word to book
	word = words[pos].replace('_', '')
	if capitalize:
		word = word.title()
		capitalize = False
	book += word
	
	# random punctuation
	if random.random() < chance_comma:
		book += ','
	elif random.random() < chance_period:
		book += '.'
		capitalize = True

	# random new paragraph (be sure to add a period first)
	if random.random() < chance_newline:
		book += '.\n\n'
		capitalize = True
	else:
		book += ' '

# add a period at the end
if book[:-2] not in '.,':
	book += '.'

# print results and save
print book
with open(output_filename, 'a') as file:
	file.write(book)

# done!
print '\n- - - - - -\n'
print '"' + output_filename + '" saved...\n\nDONE!\n\n\n'
