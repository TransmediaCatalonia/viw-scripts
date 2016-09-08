#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# Fills the Tokens' Tier of an eaf file with the tokens from a conLL file (stanford/freeling ...). 
# Checks that the eaf file and the conLL file have the same 'utterances' 
# (eaf's Audio Description = sentences in Conll) and that the Tokens' Tier is empty.
#
# usage: $ tokenize.py elanFile.eaf conllFile.txt
#
# output is written in a new eaf file: elanFile-Tokens.eaf
# Note!!! look for "CHECK!!" and configure as you need
# if miss-alignments between eaf and freeling ## uncomment to chechk miss-alignments
#-----------------------------------------------------------------------------------


import sys
import pympi    # Imports pympi to work with elan files
from shutil import copyfile

# Specify file path
args = sys.argv
elan_file_path = args[1]
freeling = args[2]

# Initialize the elan file
eaf = pympi.Elan.Eaf(elan_file_path)


###  reads file by paragraph  (sentences are one token per line, so sentences = paragraph)
def paragraphs(lines, is_separator=str.isspace, joiner=''.join):
    paragraph = [  ]
    for line in lines:
        if is_separator(line):
            if paragraph:
                yield joiner(paragraph)
                paragraph = [  ]
        else:
            paragraph.append(line)
    if paragraph:
        yield joiner(paragraph)

def getKey(item):
    return item[1]


### reads Freeling file into tags
def parseFreeling(freeling):
   # reads Freeling file into lines    
   with open(freeling) as f:
      lines = f.read().splitlines(True)

   # puts paragraphs in tags    
   tags = [] 
   for p in paragraphs(lines):  
      p= p.decode('utf-8')
      tags.append(p)
   return tags



### Add annotations 
def annotate(sentencesSorted):
   for sentence in sentencesSorted:
      #print sentence ## sentence from AD
      refId = ""
      # align sentences & tags
      i = sentencesSorted.index(sentence)
      line = tags[i] ## corresponding freeling annotated sentence (tabular mode)
      #print line 
      # split lines by \n to get tokens and remove last empty
      tokens = line.split('\n')
      tokens.pop()
      #print tokens ## freeling annotated sentence 
      # get id (refId) of referenced Annotation in AD-unit according to time in sentences

      time = sentence[0]
      for aid, (begin, end, _, _) in eaf.tiers['AD-unit'][0].items():
               begin = eaf.timeslots[begin]
               if begin == time: 
                   #print('AI',aid)
                   refId = aid
                   break
      # add token info to tokens annotation
      for token in tokens:
         # initialise empty ids list
         ids = []
         # split token into columns (form, lemma, posTag, ...)
         columns = token.split('\t')
	 
         # get existing annotations in Tokens
         ann = eaf.tiers['Tokens'][1]
	 #print('TOKEN',ann)
         # if ann then get ids and make a sorted list (we'll need the highest one)
         if ann:
            # key value in ann = {'a10321': ('a1', '1', None, None)}
            for k, v in ann.items():
               if v[0] == refId:  
                   id = k[1:]
                   id = int(id)
                   ids.append(id)
            ids.sort(reverse=True)
            ##print('KEY0T',columns[1],len(ids))
         # we don't need PREVIOUS_ANNOTATION=id for first annotation    
         if len(ids) > 0:
            previous = 'a' + str(ids[0])
            ##print('KEY1T',time, columns[1],previous)
            eaf.add_ref_annotation('Tokens','AD-unit',time, columns[0],previous) ### CHECK!! we need the 'form': stanford columns[1], freeling columns[0]
         else:
	    ##print('KEY3T',time, columns[1])
            eaf.add_ref_annotation('Tokens','AD-unit',time, columns[0]) ### CHECK!! we need the 'form': stanford columns[1], freeling columns[0]
            #eaf.add_ref_annotation('AD-Focus','AD-unit',time, columns[3])
          
      #print("----------")

### Checks that the tabular file with annotations and the Elan file have the same number of utterances
def checkAlignment(sentencesSorted):
   for sentence in sentencesSorted:
      freeling = ""
      # align sentences & tags
      i = sentencesSorted.index(sentence)
      line = tags[i]
      # split lines by \n to get tokens and remove last empty
      tokens = line.split('\n')
      tokens.pop()
      for token in tokens:
         # split tonek into columns (form, lemma, posTag, ...)
         columns = token.split('\t')
         freeling = freeling + ' ' + columns[0]              ### CHECK!! we need the 'form': stanford columns[1], freeling columns[0]
      
      s = sentence[2]
      s = s.replace(' ','')
      freeling = freeling.replace(' ','')
      freeling = freeling.replace('/','.')
      freeling = freeling.replace('_','')
      freeling = freeling.replace("'",'?')
      ## uncomment following lines to chechk miss-alignments
      ##if (freeling == s):
         ##print(i,'OK') 
      ##else:
         ##print(i,s,freeling) 

### Checks Tokens Tier is empty
def checkIfTokens():
   ann = eaf.get_ref_annotation_data_for_tier('Tokens')
   if len(ann) > 0:
	print "File already has Tokens!!! I quit, use deleteAnnotations.py to delete them"
        quit()

#--------------------------------------------------------------------------------------

if __name__ == '__main__':

   ### Get tabular file wit annotations (PoS) into tags 
   tags = parseFreeling(freeling)
   print ('Num sentences in Freeling file: ' , len(tags))

   ### Get 'Sentences' from eaf file & sort them (they come unnordered!!)
   sentences = eaf.get_annotation_data_for_tier('AD-unit')
   print ('Num sentences in eaf file: ' , len(sentences))
   sentencesSorted = sorted(sentences, key=getKey)
   #print("Freeling",tags)
   #print("Elan",sentencesSorted)

   ### check alignment between source AD Tier in the eaf file and the Freeling/Stanford tabular file
   checkAlignment(sentencesSorted)

   ### checks if Tokens Tier is empty (if already filled in with tokens warms and quits)
   checkIfTokens()

   ### Annotate sentences in the eaf file with tokens from the Freeling/Stanford tabular file
   annotate(sentencesSorted)

   ### Write the results to file with the -Tokens suffix
   eaf.to_file(elan_file_path.replace('.eaf', '-Tokens.eaf'))
   

