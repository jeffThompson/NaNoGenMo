
'''
REGEX TESTS
Jeff Thompson | 2013 | www.jeffreythompson.org

Testing lots of regex for fixing up algorithmic text.

'''

import re

# ADD QUOTES IF '[pronoun] said' IS IN THE SENTENCE
s = 'This should have no quotes. This one should he said. But this one should not. Neither should this. But this one should she asked. He asked this is different.'
pronouns = '(he|she|it)'
pronouns_upper = '(He|She|It)'
said = '(said|whispered|yelled|commanded|urged|plead|muttered)'
asked = '(asked|queried|inquired|demanded|begged)'
m = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + said + '\.', r'. "\1," \2 \3.', s)
m = re.sub(r'\.\W' + pronouns_upper+ ' ' + said + ' ([^\.]*?)\.', r'. \1 \2, "\3."', m)
m = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + asked + '\.', r'. "\1?" \2 \3.', m)
m = re.sub(r'\.\W' + pronouns_upper + ' ' + asked + ' ([^\.]*?)\.', r'. \1 \2, "\3?"', m)
m = re.sub(r'"(\b[a-z])', lambda pat: '"' + pat.group(1).upper(), m)
print ('\n' * 2) + m + ('\n' * 3)


# ADD SPACES TO TITLE
m = 'TheWarOfTheWorlds'
m = re.sub(r'([a-z])([A-Z])', r'\1 \2', m)
print m + ('\n' * 3)


# SPLIT WORDS, KEEP APOSTROPHES, CHANGE DASHES TO SPACES
sentence = '''John's favorite-food was tofu. He thought it was delicious, but only using his mother's recipe'''
sentence = re.sub(r'-', ' ', sentence)
for word in sentence.split(' '):
	word = re.sub(r'[^\'\w]', '', word)
	print word
print ('\n' * 3)


# GET RID OF WEIRD PUNCTUATION DUPLICATES
s = '''This,,. will,,, not.. work??.. very''    'well .. he's, , , said\n\n sadly can't '''
s = re.sub(r',+\.+', '.', s)			# , followed by .
s = re.sub(r'\?+\.+', '?', s)			# ? followed by .
s = re.sub(r'\s+\.+', '.', s)			# space before .
s = re.sub(r'\s+,+', ',', s)			# space before ,
s = re.sub(r',{2,}', ',', s)						# more than 1 ,
s = re.sub(r'\.{2,}', '.', s)						# ditto .
s = re.sub(r'[^a-zA-Z]\'+', '', s)			# remove ' at start of word
s = re.sub(r'\'+[^a-zA-Z]', '', s)			# ditto end of word
s = re.sub(r'[^\S\r\n]{2,}', ' ', s)		# 2 or more spaces (ignore \n and \r)
print s + ('\n' * 3)


# MAKE SURE ALL SENTENCES ARE CAPITALIZED
s = '''This sentence is capitalized. this one should not be. But this one is.'''
s = re.sub(r'(\.|\?) ([a-z])', lambda pat: pat.group(1) + ' ' + pat.group(2).upper(), s)
print s + ('\n' * 3)


# CAPITALIZE ALL MAIN CHARACTERS
s = 'Then sam ate gandalf.'
characters = [ 'gollum', 'frodo', 'gandalf', 'sam' ]
char_regex = '(' + '|'.join(char for char in characters) + ')'
s = re.sub(char_regex, lambda pat: pat.group(1).title(), s)
print s + ('\n' * 3)


# CAPITALIZE INSTANCES OF THE WORD 'I'
s = '''i and i'll and i'm'''
s = re.sub(r'\bi(\b|\')', 'I\1', s)
print s + ('\n' * 3)


# FIX ODDLY CAPITALIZED LETTERS
s = '''He'Ll know this sentence can'T be right.'''
s = re.sub(r'\'([A-Z].*?)\b', lambda pat: '\'' + pat.group(1).lower(), s)
print s + ('\n' * 3)


# CHANGE A TO AN AND VICE VERSA
s = 'A ox and a apple. An dog too.'
s = re.sub(r'\b(A|a)\b ([aeiouAEIOU])', r'\1n \2', s)
s = re.sub(r'\b(An|an)\b ([^aeiouAEIOU])', lambda pat: pat.group(1)[0] + ' ' + pat.group(2), s)
print s + ('\n' * 3)


# FIX MISSING PERIODS
s = 'This should have a period\n\nBut it did not!'
s = re.sub(r'(\b[^\.]\n+)', r'.\1', s)
print s + ('\n' * 3)


# NUMBERS AS TEXT REPRESENTATIONS
s = 'A number 1, a 48, chapter 13, #5, 16 candles, part 1'
s = re.sub(r'(?<!(chapter)) \b(1)\b', r' one', s)
s = re.sub(r'(?<!(chapter)) \b(2)\b', r' two', s)
s = re.sub(r'(?<!(chapter)) \b(3)\b', r' three', s)
s = re.sub(r'(?<!(chapter)) \b(4)\b', r' four', s)
s = re.sub(r'(?<!(chapter)) \b(5)\b', r' five', s)
s = re.sub(r'(?<!(chapter)) \b(6)\b', r' six', s)
s = re.sub(r'(?<!(chapter)) \b(7)\b', r' seven', s)
s = re.sub(r'(?<!(chapter)) \b(8)\b', r' eight', s)
s = re.sub(r'(?<!(chapter)) \b(9)\b', r' nine', s)
s = re.sub(r'(?<!(chapter)) \b(10)\b', r' ten', s)
s = re.sub(r'(?<!(chapter)) \b(11)\b', r' eleven', s)
s = re.sub(r'(?<!(chapter)) \b(12)\b', r' twelve', s)
s = re.sub(r'(?<!(chapter)) \b(13)\b', r' thirteen', s)
s = re.sub(r'(?<!(chapter)) \b(14)\b', r' fourteen', s)
s = re.sub(r'(?<!(chapter)) \b(15)\b', r' fifteen', s)
s = re.sub(r'(?<!(chapter)) \b(16)\b', r' sixteen', s)
s = re.sub(r'(?<!(chapter)) \b(17)\b', r' seventeen', s)
s = re.sub(r'(?<!(chapter)) \b(18)\b', r' eighteen', s)
s = re.sub(r'(?<!(chapter)) \b(19)\b', r' nineteen', s)
print s + ('\n' * 3)





