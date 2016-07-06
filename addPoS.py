#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import xml.etree.ElementTree as et
import csv
sys.stdout.encoding
'UTF-8'
args = sys.argv

outFile =  args[1] + "-ALL.eaf"
freeling = args[2]


# parse elan file
tree = et.parse(args[1])

# read Freeling file
tags = []
lemmas = []
semantic = []

#with open('stanford.txt','rb') as f:
with open(freeling,'rb') as f:
   freeling = csv.reader(f,delimiter='\t')
   for line in freeling:
      if line == []:
         pass
      else:
	 #e = line[1].decode("utf-8").encode("latin-1").decode("utf-8")
	 #ee = line[1].decode("utf-8").encode('raw_unicode_escape').decode('utf-8')
         #U = line[1].decode('utf8')
         #UU = U.encode('utf8')
         #print(line[1])#,e,ee,U,UU)
         tags.append(line[2].decode('utf-8'))    ###
	 lemmas.append(line[1].decode('utf-8'))  ###
         if len(line) > 6:
	     semantic.append(line[6].decode('utf-8'))  ###
	 else: semantic.append('-')  ###
	 

#print tags
#print lemmas

# add pos tags
i = 0
for ann in tree.findall("TIER[@TIER_ID='PoS']/ANNOTATION/REF_ANNOTATION/ANNOTATION_VALUE"):
  row = tags[i]
  ann.text = row.encode('utf-8')
  i = i + 1

# add lemmas
j = 0
for ann in tree.findall("TIER[@TIER_ID='Lemma']/ANNOTATION/REF_ANNOTATION/ANNOTATION_VALUE"):
  row = lemmas[j]
  ann.text = row
  j = j + 1

# add lemmas
k = 0
for ann in tree.findall("TIER[@TIER_ID='Semantic']/ANNOTATION/REF_ANNOTATION/ANNOTATION_VALUE"):
  row = semantic[k]
  ann.text = row
  k = k + 1

tree.write(outFile, encoding="UTF-8",xml_declaration=True)

