


# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 22:01:04 2022

@author: Oscar
#listening to Lana <3
"""

#WARNING
#This code will not work as written but can be adapted with careful use. 
#This code creates files that are used to operate a SELECT SERIES instrument. 
#Only use this code in a separate folder on copies of methods and manually check the output before using the method file on a live instrument. 
#Always start with a copy of a method file that has been demonstrated to function correctly. 
#This tool should only be used when necessary, by individuals confident with coding and file manipulation. 
#Whilst this code worked correctly for the published experiments, the authors of this work take no responsibility for any damage done to any instrument by anyone who applies this code or a similar approach in their own work.


import csv
import xml.etree.ElementTree as ET

with open('Cryptophane_ions.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    linecount = 0
    for row in csv_reader:
        if linecount==0:
            print('titles')
            linecount=linecount+1
        else:
            name=row['Name']
            mz1=row['1+']
            mz2=row['2+']
            mz1str=str(mz1)
            mz2str=str(mz2)
            filenamestr1=str(name+"_"+mz1str+".xml")
            filenamestr2=str(name+"_"+mz2str+".xml")

THIS COMMENT HAS BEEN UNCOMMENTED TO BREAK THIS CODE. ONLY COMMENT THIS ONCE YOU ARE CONFIDENT YOU HAVE PROVIDED THE APPROPRIATE .csv AND.XML.

            tree=ET.parse('20220728_3PA_10pass_MSMS373.xml')
            myroot=tree.getroot()
        
            for MS in myroot.iter('Function'):
                function=MS
                for setting in function.iter('Settings'):
                    h=setting.findall('Setting')
                    count=0
                    for item in h:
                        
                        z=item.attrib
                        if 'SetMass' in z.values():
                            saved=z
                            savedcount=count
                            print(z)
                            break
                        count=count+1
                    p=h[savedcount]     
                    p.set('Value',mz1str)
                    tree.write(filenamestr1)  
                    p.set('Value',mz2str)
                    tree.write(filenamestr2)
            print(name)          
            linecount=linecount+1

