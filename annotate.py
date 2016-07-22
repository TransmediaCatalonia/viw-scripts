#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# Adds annotations to an eaf file.
# Annotations are read from tabular file (conLL format).
# Annotations go to Token's children Tiers (pos, lemma and semantics)
#
# usage: $ annotate.py elanFile.eaf conllFile.txt
#
# output is written in a new eaf file: elanFile-Annotated.eaf
#
# This assumes the conll file is like this: "form lemma postag ..... semtag" (where semtag = the last column of a tabular file)
# If you have any other format, look for "CHECK!!" and configure as you need
#
# Return as pretty-printed XML has character encoding problems
# better use "xmllint --format" on output file to get an indented version
#-----------------------------------------------------------------------------------


from xml.dom import minidom
import sys
import xml.etree.ElementTree as et
import csv

sys.stdout.encoding
'UTF-8'
args = sys.argv


outFile =  args[1].replace('.eaf', '-Annotated.eaf')
freeling = args[2]

elan = et.parse(args[1])   # Parses ELAN 'eaf' file
root = elan.getroot()

tags = []
lemmas = []
semantics = []

## Gets Ids from Tokens Tier, we need them in the 'ANNOTATION_REF' attributes of dependent TIERS (lemma,PoS,semantics)
def getReferenceIds():
   ids = []
   global elan
   for ann in elan.findall("TIER[@TIER_ID='Tokens']/ANNOTATION/REF_ANNOTATION"):
      id = ann.get('ANNOTATION_ID')
      #print id
      ids.append(id)
   # sort ids (crucial!! we always get things unordered....)
   ids.sort(key=lambda x: '{0:0>8}'.format(x).lower())
   return ids

# Reads 'tabular' file with annotations to be included in the ELAN file (PoS, lemma, semantic, ...)
def readAnnotationFile(freeling):
   global tags, lemmas, semantics 

   with open(freeling,'rb') as f:
      freeling = csv.reader(f,delimiter='\t')
      for line in freeling:
         if line == []:
            pass
         else:
            tags.append(line[2].decode('utf-8'))    ### CHECK!!
   	    lemmas.append(line[1].decode('utf-8'))  ### CHECK!!
            if len(line) > 2:
		i = len(line)-1
	        semantics.append(line[i].decode('utf-8'))  ### CHECK!!
	    else: semantics.append('-')  ###
	 
   #print tags
   #print lemmas
   #print semantics

# provides an 'elan' id (receives and int and returns a string (a + integer)
def provideId(i):
   Id = "a" + str(i)
   return Id

# checks if Token has PREVIOUS_ANNOTATION
# <ANNOTATION><REF_ANNOTATION ANNOTATION_ID="a182" ANNOTATION_REF="a5" PREVIOUS_ANNOTATION="a181">
def checkPrevious(id):
   token = root.find("TIER[@TIER_ID='Tokens']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID='"+id+"']")
   previous = token.get('PREVIOUS_ANNOTATION')
   return previous

## annotates ELAN file (fill PoS, lemma and semantic Tiers with informtion from tabular file)
def annotate(lastId):
   global root
   k = int(0)
   i = lastId + 5

   # we run the Tokens ids for each annotation layer (Tier) as we want succesive Id's to easy 'PREVIOUS_ANNOTATION' assignment...
   # semantics tier
   for id in ids: 
      #####previous = checkPrevious(id)
      row = semantics[k]    
      i = i + 1
      semId = provideId(i)
      semTier = root.find("TIER[@TIER_ID='Semantic']")
      ann = et.SubElement(semTier, "ANNOTATION")
      myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": semId}
      #####if previous is None:
               #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": semId}
            #####else:
               #####previousId = provideId(i-1)
               #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": semId, 'PREVIOUS_ANNOTATION' : previousId}
      ref_ann = et.SubElement(ann, "REF_ANNOTATION", attrib=myattributes )
      value = et.SubElement(ref_ann,"ANNOTATION_VALUE")
      value.text = row 
      k = k + 1

   # Lemma tier
   k = int(0)
   for id in ids: 
            #####previous = checkPrevious(id)
      lemma = lemmas[k]        
      i = i + 1
      lemmaId = provideId(i)
      lemmaTier = root.find("TIER[@TIER_ID='Lemma']")
      annLemma = et.SubElement(lemmaTier, "ANNOTATION")

      myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": lemmaId}
            #####if previous is None:
               #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": lemmaId}
            #####else:
               #####previousId = provideId(i-1)
               #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": lemmaId, 'PREVIOUS_ANNOTATION' : previousId}
      ref_annLemma = et.SubElement(annLemma, "REF_ANNOTATION", attrib=myattributes )
      valueLemma = et.SubElement(ref_annLemma,"ANNOTATION_VALUE")
      valueLemma.text = lemma #lemma.encode('utf-8')
      k = k + 1

   # PoS tier
   k = int(0)
   for id in ids:
      
      #####previous = checkPrevious(id)
      pos = tags[k]
      # PoS tier
      i = i + 1
      posId = provideId(i)
      posTier = root.find("TIER[@TIER_ID='PoS']")
      annPos = et.SubElement(posTier, "ANNOTATION")

      myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": posId}
      #####if previous is None:
         #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": posId}
      #####else:
         #####previousId = provideId(i-1)
         #####myattributes = {'ANNOTATION_REF': id, "ANNOTATION_ID": posId, 'PREVIOUS_ANNOTATION' : previousId}
      ref_annPos = et.SubElement(annPos, "REF_ANNOTATION", attrib=myattributes )
      valuePos = et.SubElement(ref_annPos,"ANNOTATION_VALUE")
      valuePos.text = pos
      k = k + 1

   return(i)


## Updates LastId in elan file
def updateLastId(id):
  prop = root.find("HEADER/PROPERTY[@NAME='lastUsedAnnotationId']")
  prop.text = str(id)
  print("Updated last id:", id)


## Return a pretty-printed XML string for the Element. 
## (it does not work, character encoding problems!!!!... better use xmllint --format on output file)
def prettify(elem):
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


##### Main---------------------------------------------------------------------------------

if __name__ == '__main__':

   # read Annotation file freeling/standford)
   readAnnotationFile(freeling)
   
   # gets Tokens Ids (used in ANNOTATION_REF of dependent Tiers)
   ids = getReferenceIds()

   # sets last Id in elan file, (used when generating news ids..)
   # we cannot trust the HEADER/PROPERTY[@NAME='lastUsedAnnotationId, (it is not updated whith pympi...) so we relay on Tokens:
   # we annotate after tokenising, this means that the last id in Tokens is the last id.

   lastId = ids[-1].replace("a", "")
   

   print ("referencIds:",len(ids))
   print ("lemmas:",len(lemmas))
   print ("semantic:",len(semantics))
   print ("tags:",len(tags))
   print ("Last id:",lastId)

   # Adds annotations in ELAN
   newLast = annotate(int(lastId))

   # Updates last Id in ELAN (HEADER/PROPERTY[@NAME='lastUsedAnnotationId) just in case we needed in the future...
   updateLastId(newLast)
   #et.dump(root)

   elan.write(outFile, encoding="UTF-8",xml_declaration=True)

   #print(et.tostring(ref_ann))


