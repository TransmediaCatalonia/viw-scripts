#!/usr/bin/env bash
#
#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# cats 'freeling' files in one single file ready to be indexed in CQP.
#
# each file is included in <text> tags.
#
# sentences in conll file are enclosed between <s> tags.
#
# usage: $ ./freeling2CQO.sh 'path_to_freeling_dir'
#
# output is written in a new file cqp.txt
#-----------------------------------------------------------------------------------

if [ ! $# -ge 1 ]; then
  echo Usage: `basename $0` 'path_to_freeling_dir'
  echo 
  exit
fi

path=$1



for file in $path
do
    echo doing $file
	awk 'BEGIN { OFS = "\t"} {print $1,$2,$3,$7}' $file | sed "1s|^|<text id=\'$file\'>\n<s>\n|" | sed "s/\t\t\t//" | 
        sed 's/Fp\t$/Fp\t\n<\/s>\n<s>/' | sed '/^$/d' | sed 's/Fp\t-/Fp\t-\n<\/s>\n<s>/'>> cqp.txt
    echo done $file  
done
