#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# counts lines, sentences, words, and gives different statistical measures of a txt file (sentences.txt in data/ subdir)
#
# usage: $ python CountWords.py input_path
#
# output is written in countWords.txt
#
#-----------------------------------------------------------------------------------

import re
import sys
sys.stdout.encoding
'UTF-8'
args = sys.argv

inFile = args[1] + "/data/sentences.txt"
outFile =  args[1] + "countWords.txt"

### some stats functions
def avg(list):

	sum = 0
	for elm in list:
		sum += elm
	return str(sum/(len(list)*1.0))
	
def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0


# set counters to zero

lines, blanklines, sentences, words = 0, 0, 0, 0
sentsXline = list()
wordsXline = list()
wordsXsentence = list()

#print '-' * 50

try:

  # input file
  filename = inFile
  textf = open(filename, 'r')

except IOError:

  print 'Cannot open file %s for reading' % filename

  import sys
  sys.exit(0)

# reads one line at a time

for line in textf:

  #print line,   # test

  if line.startswith('\n'):

    blanklines += 1
  elif line.startswith('###'):

    blanklines += 1
  else:
    lines += 1
    # we cannot assume that each sentence ends with . or ! or ?
    # some things to do befor counting sentence separators:
    # 1) replace ... by . 
    line = line.replace('...', '.')
    # 2) deals with endings like bla.' or bla." (removes dot before final quotations)
    line = line.replace('."\n','"\n')
    line = line.replace(".'\n","'\n")
    # 3) removes new line at the end of line    
    l = line.rstrip()
    # get last character
    end = l[-1:]
    
    if end == '.' or end == '!' or end == '?':
        # so simply count these characters
        sentences += line.count('.') + line.count('!') + line.count('?') + line.count('/')
        sent = line.count('.') + line.count('!') + line.count('?') + line.count('/')
    else:
        # simply count these characters + 1 (for the missing final marker) 
        sentences += line.count('.') + line.count('!') + line.count('?') + line.count('/')
        sentences += 1
        sent = line.count('.') + line.count('!') + line.count('?') + line.count('/')
        sent += 1

    sentsXline.append(sent)

    # create a list of words (tempwords), use None to split at any whitespace regardless of length
    # so for instance double space counts as one space

    tempwords = line.split(None)
    wordsXline.append(len(tempwords))
    #print tempwords  # test
    # word total count
    words += len(tempwords)

    # words x sentence
    delimiters = ".", "?", "!", "/"
    regexPattern = '|'.join(map(re.escape, delimiters))
    items = re.split(regexPattern, line)
    items.pop()
    for i in items:
        temptokens = i.split(None)
    	wordsXsentence.append(len(temptokens))


textf.close()

mode = sorted(wordsXline, key=wordsXline.count)[-1]
modeS = sorted(wordsXsentence, key=wordsXsentence.count)[-1]

print "Paragraphs:	", lines
print "Sentences:	", sentences
print "Words:	", words
print "SentencesXpar:	", sentsXline
print "WordsXpar:	", wordsXline
print "Avg_WordsXpar:	", avg(wordsXline)
print "Median_WordsXpar:	", median(wordsXline)
print "Min_WordsXpar:	", min(wordsXline)
print "Max_WordsXpar:	", max(wordsXline)
print "Mode_WordsXpar:	", mode
print "Range_WordsXpar:	" + str(max(wordsXline) - min(wordsXline))

print "WordsXsentence:	", wordsXsentence
print "Avg_WordsXsentence:	", avg(wordsXsentence)
print "Median_WordsXsentence:	", median(wordsXsentence)
print "Min_WordsXsentence:	", min(wordsXsentence)
print "Max_WordsXsentence:	", max(wordsXsentence)
print "Mode_WordsXsentence:	", mode
print "Range_WordsXsentence:	" + str(max(wordsXsentence) - min(wordsXsentence))

