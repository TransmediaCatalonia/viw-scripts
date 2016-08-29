#!/usr/bin/env bash
#
# Runs the English PCFG parser on one or more files

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'file(s)'
  echo
  exit
fi


scriptdir=`dirname $0`

java -mx150m -cp "$scriptdir/*:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $* -conllx 

## use this instead if you also want the dependency tree (in temp.txt).
## TEMP=temp.txt
## scriptdir=`dirname $0`

## java -mx150m -cp "$scriptdir/*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser \
## -outputFormat "penn"  edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $* > temp.txt

## java -mx150m -cp "$scriptdir/*:" edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile $TEMP -conllx 
