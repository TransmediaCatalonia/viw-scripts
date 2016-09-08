#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# Reads eaf file and creates a tabular a file (coneLL format) with form, lemma, postag, semantics
#
# usage: $ eaf2conll.py elanFile.eaf > outfile
#
# 
#-----------------------------------------------------------------------------------


import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import xml.etree.ElementTree as et


# Specify file path
args = sys.argv
elan_file_path = args[1]

# Initialize the elan file
elan = et.parse(args[1])   # Parses ELAN 'eaf' file
root = elan.getroot()


## Gets Ids from ADs (we need them ordered)
def getIds():
   ids = []
   global elan
   for ann in root.findall("TIER[@TIER_ID='AD-unit']/ANNOTATION/ALIGNABLE_ANNOTATION"):
      id = ann.get('ANNOTATION_ID')
      #print id
      ids.append(id)
   # sort ids (crucial!! we always get things unordered....)
   ids.sort(key=lambda x: '{0:0>8}'.format(x).lower())
   return ids

## Gets Ids from Tokens Tier, we need them ordered
def getReferenceIds(au):
   ids = []
   global elan
   for ann in root.findall("TIER[@TIER_ID='Tokens']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='" + au + "']"):
      id = ann.get('ANNOTATION_ID')
      #print id
      ids.append(id)
   # sort ids (crucial!! we always get things unordered....)
   ids.sort(key=lambda x: '{0:0>8}'.format(x).lower())
   return ids

#---------------------------------------

# gets AudioDescriptions id in order (we assume that ids are ordered)
ads = getIds()

# for each AU, gets corresponding Tokens in order
for au in ads:
   tokensIds = getReferenceIds(au)
   for i in tokensIds:
      # gets 'from' from Tokens Tier
      token = root.find("TIER[@TIER_ID='Tokens']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID='"+i+"']")
      t = token.find('ANNOTATION_VALUE').text.decode('utf-8')
      
      # gets 'pos tag' from Tokens Tier
      pos = root.find("TIER[@TIER_ID='PoS']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='" + i + "']")
      p = pos.find('ANNOTATION_VALUE').text
      # gets 'lemma' from Lemma Tier
      lemma = root.find("TIER[@TIER_ID='Lemma']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='" + i + "']")
      l = lemma.find('ANNOTATION_VALUE').text.decode('utf-8')
      # gets 'semantic' from Semantic Tier
      sem = root.find("TIER[@TIER_ID='Semantic']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='" + i + "']")
      s = sem.find('ANNOTATION_VALUE').text

      
      print "%s\t%s\t%s\t%s" % (t,l,p,s)
      
   print "\n"

