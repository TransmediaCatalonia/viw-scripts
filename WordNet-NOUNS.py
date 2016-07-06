#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import sys
import urllib
import re

sparql = SPARQLWrapper("http://lodserver.iula.upf.edu/sparql")
args = sys.argv
lines = [line.split() for line in open(args[1])]
lang = args[2] 
iri = "<http://ewn" + lang + ".edu>"

outFile = args[1][:-4] + "-2.txt"
f1=open(outFile, 'w+')

def main(lines,lang):
    global f1
    
    noun = re.compile('^NC.*')
    
    for l in lines:     
       if len(l) > 1 and noun.match(l[2]):				### 'common' verb form
            wordform = unicode( l[1], "utf-8" )
            #print l
            results = getSparql(wordform,iri,'noun')
            #print results
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
	        #print sumo
		if sumo[1] == "BodyPart" or sumo  == "Clothing":
                	l.append(sumo[1])
            else:
                l.append("null")
       
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
    #print query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results)



main(lines,iri)
