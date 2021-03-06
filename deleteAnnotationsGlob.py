#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# removes annotations Tokens + dependent Tiers in eaf files matching a given path pattern
#
# usage: $ python deleteAnnotationsGlob.py "file path pattern"
#
# example  python deleteAnnotationsGlob.py  "../data/What-CA/*/*.eaf"
#
# ****** Warning: the path needs to be between quotes!!
# 
# the original eaf file is modified and a .bak file is created
#-----------------------------------------------------------------------------------

import glob
import os
import sys
import pympi    # Imports pympi to work with elan files
import shutil   # used to copy file

# Specify file path
args = sys.argv
elan_path = args[1]



def doit(elan_file_path):
   # Copies original eaf file into a bak file
   bakfile = elan_file_path + '.BAK'
   shutil.copy2(elan_file_path, bakfile)

   # Initialize the elan file
   eaf = pympi.Elan.Eaf(elan_file_path)

   # Gets Tokens children
   children = eaf.get_child_tiers_for('Tokens')

   # Removes Annotations in Tokens children
   for child in children:
      eaf.remove_all_annotations_from_tier(child, clean=True)

   # Removes Annotations in Tokens tier
   eaf.remove_all_annotations_from_tier('Tokens', clean=True)

   # Write the results to file with the -Tokens suffix
   eaf.to_file(elan_file_path)

   # Removes the bak file created by pympi API
   remove = elan_file_path + '.bak'
   os.remove(remove)

#------------------------------------------------------------------------------

files = glob.glob(elan_path)

for f in files:
   doit(f)
   print(f, "done")


