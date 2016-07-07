#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# Adds WordNet semantic classes to freeling files (for Nouns, Verbs and Adjectives)
# 
# This script uses the IULA sparql server: http://lodserver.iula.upf.edu/sparql
#
# No semantic dissambiguation is performed (manual checking required...)
# 
#-----------------------------------------------------------------------------------


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
    verb = re.compile('^VM[^P].*')
    verbP = re.compile('^VMP.*')
    aux =  re.compile('^VA.*')
    adj = re.compile('^AQ.*')
    noun = re.compile('^NC.*')
    soyAux = "no"
    for l in lines:     
       if len(l) > 1 and verb.match(l[2]):				### 'common' verb form
            wordform = unicode( l[1], "utf-8" )
            #print l
            results = getSparql(wordform,iri,'verb')
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
                l.append(sumo[1])
            else:
                l.append("null")
       elif len(l) > 1 and aux.match(l[2]):				### aux!!!
             soyAux = "yes"
       elif len(l) > 1 and verbP.match(l[2]) and soyAux == "yes" :	### 'ha fet' 
            wordform = unicode( l[1], "utf-8" )
            #print("HA", l)
            results = getSparql(wordform,iri,'verb')
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
                l.append(sumo[1])
            else:
                l.append("null")
       elif len(l) > 1 and verbP.match(l[2]):			### preocupat 
            wordform = unicode( l[1], "utf-8" )
            #print("HA", l)
            results = getSparql(wordform,iri,'verb')
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
                l.append("A-" + sumo[1])
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
       elif len(l) > 1 and noun.match(l[2]):				### 'nouns'
            wordform = unicode( l[1], "utf-8" )
            #print l
            results = getSparql(wordform,iri,'noun')
            #print results
            if len(results["results"]["bindings"]) > 0:
                sumo = results["results"]["bindings"][0]["plus"]["value"].split("#")
	        #print sumo
		if sumo[1] == "BodyPart" or sumo[1]  == "Clothing":
                	l.append(sumo[1])
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
    #print query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results)



main(lines,iri)
