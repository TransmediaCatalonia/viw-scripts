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
# usage: $ ./stanford2CQP.sh 'path_to_freeling_dir'
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
	cat $file | sed "1s|^|<text id=\'${file//[_-]}\'>\n<s>\n|" |
	
        sed 's/^$/\n<\/s>\n<s>/'  >> cqp.txt

    echo done $file  
done


## adds final closing tag nad ...
cat cqp.txt | sed '$ a </text>' | tr '\n' '\f' | sed -e 's/-\f<text/-\f<\/s>\f<text/g' | sed -e 's/<s>\f<text/\f<text/g' |
sed 's/<s>\f<\/text/\f<\/text/g' | tr '\f' '\n' | sed '/^$/d' > tmp.txt


mv tmp.txt cqp.txt
