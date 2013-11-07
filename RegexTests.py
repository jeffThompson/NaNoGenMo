
'''
REGEX TESTS
Jeff Thompson | 2013 | www.jeffreythompson.org

'''

import re

# ADD QUOTES
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


# REMOVE SPACES
s = 'This\nAnd this.'
m = re.sub(r'\n.*?(\b[a-zA-Z])', lambda pat: '\n' + pat.group(1).upper(), s)
print m + ('\n' * 3)


# ADD SPACES TO TITLE
m = 'TheWarOfTheWorlds'
m = re.sub(r'([a-z])([A-Z])', r'\1 \2', m)
print m + ('\n' * 3)


# SPLIT WORDS, KEEP APOSTROPHES
sentence = '''John's favorite food was tofu. He thought it was delicious, but only using his mother's recipe'''
for word in sentence.split(' '):
	word = re.sub(r'[^\'\w]', '', word)
	print word
print ('\n' * 3)


# GET RID OF WEIRD PUNCTUATION DUPLICATES
s = '''This,,. will,,, not.. work??.. very''    'well .. he's, , , said\n\n sadly'''
print s + '\n'
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









