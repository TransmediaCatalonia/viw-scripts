#!/usr/bin/env bash 
#
#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# Adds the linguistic annotations in a 'conll file' into an 'eaf file'
#
# pipe:  tokenise.py | annotate.py | xmllint --format 
#
# usage: $ ./conll2eaf.sh 'path_to_eaf_file(s)' 'conll_file'
#
# example: $ ./conll2eaf.sh '../data/What-CA/*/*.eaf' 'freeling-2.txt'
#
# (path needs to be between quotes; assumes conll_file is in data subdir)
#-----------------------------------------------------------------------------------



if [ ! $# -ge 2 ]; then
  echo Usage: `basename $0` 'path' 'conLL_file_name'
  echo 
  exit
fi


#--------------------

path=$1
freeling=$2



for file in $path
do
    
    data="/data/"

    echo doing $file $dir$data$freeling
    
    # sets tokens file   
    base=${file%.*}
    tokens="-Tokens.eaf"
    tokensfile="$base$tokens"

    # sets Annotated file
    base2=${tokensfile%.*}
    ann="-Annotated.eaf"
    annfile="$base2$ann"

    # sets bak file
    bak="-Source.BAK"
    bakfile="$file$bak"

    # sets dir file
    dir=${file%/*}
    
    # executes tokenise.py on *.eaf using 'freeling' file in data subdir
    # tokenise.py writes output in *-Tokens.eaf 
    python ./tokenise.py $file $dir$data$freeling

    if [ -f "$tokensfile" ]
    then
        echo tokenisation done  $file 
    
        # executes annotate.py on *-Tokens.eaf using 'freeling' file in data subdir
        # tokenise.py writes output in *-Tokens-Annotated.eaf
        python ./annotate.py $tokensfile $dir$data$freeling
        
        if [ -f "$annfile" ]
        then
            # makes a bak copy of original eaf file
            cp $file $bakfile

            # prittyprints *-Tokens-Annotated.eaf file overwritting the original *eaf.file (previously saved)
            xmllint --format $annfile > $file

            # removes *-Tokens.eaf and *-Tokens-Annotated.eaf files
            rm $dir/*Tokens*

            #echo 'annotation done, new ' $eaf 'created, you hava a bak copy in '$bakfile
        else
	    echo "**** $file not annotated!!."
        fi

    else
	echo "**** $file not tokenised!!."
    fi
done

ls $path

#--------------------

