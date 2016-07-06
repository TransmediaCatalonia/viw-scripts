#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import sys
import urllib
import re
import xml.etree.ElementTree as ET





sparql = SPARQLWrapper("http://lodserver.iula.upf.edu/sparql")
args = sys.argv
lines = [line.split() for line in open(args[1])]
lang = args[2] 
iri = "<http://ewn" + lang + ".edu>"

outFile = args[1][:-4] + "-2.txt"
verbsFile = args[1][:-4] + "Verbs.xml"
f1=open(outFile, 'w+')


verbs = []
print("VERBS FILE: ", verbsFile)
tree = ET.parse(verbsFile)
root = tree.getroot()

    
for sentence in root.findall('sentence'):
    for word in sentence.findall('word'):
        lemma = word.get('lemma')
        #print(lemma)
        verbs.append(lemma)


def main(lines,lang):
    global f1,verbs
    
    verb = re.compile('^VB.*')
    
    adj = re.compile('^AQ.*')
    soyAux = "no"
    for l in lines:     
       if len(l) > 1 and verb.match(l[3]):				### 'common' verb form
            wordform = verbs[0]
            #print l
            results = getSparql(wordform,iri,'verb')
            verbs.pop(0)
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
                l.append(sumo[1])
            else:
                l.append("null")
       
       
       elif len(l) > 1 and adj.match(l[2]):				### adj
            wordform = unicode( l[1], "utf-8" )
            #print l
            results = getSparql(wordform,iri,'adjective')
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
                l.append("A-" + sumo[1])
            else:
                l.append("null")
       else:
           soyAux = "no"
       f1.write('\t'.join(l))
       f1.write('\n')

def getSparql(word,iri,pos):


    head = """
prefix lemon:   <http://lemon-model.net/lemon#>
prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>

SELECT DISTINCT ?plus FROM """

    where = """
WHERE { 
	?entry lemon:canonicalForm ?form ; lexinfo:partOfSpeech lexinfo:"""
    where1 = """ ; lemon:sense ?sense .
	?form lemon:writtenRepresentation '"""
    where2 = """'. 
	?sense <http://lodserver.iula.upf.edu/euroWordNetMCR/sumo_plus> ?plus .
	}"""


    query = head + iri + where + pos + where1 + word + where2
    print query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results)



main(lines,iri)
