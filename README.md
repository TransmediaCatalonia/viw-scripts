# viw-scripts

This repository contains the scripts used to edit and manage data in the VIW project (Visual into Words http://pagines.uab.cat/viw).

Thee cqp_files subdir contains corpus files in cqp format ready to be loaded into the CWB.


####annotate.py

Adds annotations to an eaf file previously tokenised by tokenise.py.
Annotations are read from tabular file (conLL format).
Annotations go to Token's children Tiers in the eaf file (pos, lemma and semantics)

####conll2eaf.sh

Adds the linguistic annotations in a 'conll file' into an 'eaf file'

Use this when you want to annotate multiple 'eaf' files (path_to_eaf-file(s))

pipe:  tokenise.py | annotate.py | xmllint --format 

usage: $ ./conll2eaf.sh 'path_to_eaf_file(s)' 'conll_file'

example: $ ./conll2eaf.sh '../data/What-CA/*/*.eaf' 'freeling-2.txt'

####CountWords.py

counts lines, sentences, words, and gives different statistical measures of a txt file (file = sentences.txt in data/ subdir)

####deleteAnnotationsGlob.py

removes annotations Tokens + dependent Tiers in eaf files matching a given path pattern

usage: $ python deleteAnnotationsGlob.py "file path pattern"

####deleteAnnotations.py

removes annotations Tokens + dependent Tiers in selected eaf file.

####eaf2conll.py

Reads eaf file and creates a tabular a file (conLL format) with form, lemma, postag, semantics

####freeling2CQP.sh

'cats' conLL/freeling files in one single file ready to be indexed in CQP.

each file is included between 'text' tags where text/@id = file_name. 

sentences in conLL file are enclosed between 's' tags.

####lexparser.sh

This is the shell script used to run the Stanford parser.

####tokenise.py

Fills the Tokens' Tier of an eaf file with the tokens from a conLL file (stanford/freeling ...). 
Checks that the eaf file and the conLL file have the same number of 'utterances' 
(eaf's Audio Description = sentences in Conll) and that the Tokens' Tier is empty.

usage: $ tokenize.py elanFile.eaf conllFile.txt

output is written in a new eaf file: elanFile-Tokens.eaf

####WordNet.py

Adds WordNet semantic classes to freeling files (for Nouns, Verbs and Adjectives)

This script uses the IULA sparql server at http://lodserver.iula.upf.edu/sparql





