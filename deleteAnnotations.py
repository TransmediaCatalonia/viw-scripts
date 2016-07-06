#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# Marta Villegas (UAB)  VIW project (Visual into Words http://pagines.uab.cat/viw)
#
# removes annotations Tokens + dependent Tiers
#
# usage: $ deleteAnnotations.py elanFile.eaf 
#
# output is written in a new eaf file: elanFile-Tokens.eaf
#-----------------------------------------------------------------------------------


import sys
import pympi    # Imports pympi to work with elan files

# Specify file path
args = sys.argv
elan_file_path = args[1]

# Initialize the elan file
eaf = pympi.Elan.Eaf(elan_file_path)

# Gets Tokens children
children = eaf.get_child_tiers_for('Tokens')

# Removes Annotations in Tokens children
for child in children:
   eaf.remove_all_annotations_from_tier(child, clean=True)

# Removes Annotations in Tokens tier
eaf.remove_all_annotations_from_tier('Tokens', clean=True)

### Write the results to file with the -Tokens suffix
eaf.to_file(elan_file_path.replace('.eaf', '-Clean.eaf'))
