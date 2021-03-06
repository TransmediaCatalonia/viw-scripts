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
# output is written in a new file cqp.txt	sed '/^$/d' |
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
	awk 'BEGIN { OFS = "\t"} {print $1,$2,$3,$7}' $file | sed "1s|^|<text id=\'${file//[_-]}\'>\n<s>\n|" | 
	sed "s/\t\t\t//" | sed "s/\t$/\t-/" |
        sed 's/Fp\t-/Fp\t-\n<\/s>\n<s>/' | sed 's/Fit\t-/Fit\t-\n<\/s>\n<s>/' >> cqp.txt

    echo done $file  
done


## adds final closing tag nad ...
cat cqp.txt | sed '$ a </text>' | tr '\n' '\f' | sed -e 's/-\f<text/-\f<\/s>\f<text/g' | sed -e 's/<s>\f<text/\f<text/g' |
sed 's/<s>\f<\/text/\f<\/text/g' | tr '\f' '\n' | sed '/^$/d' > tmp.txt


mv tmp.txt cqp.txt
