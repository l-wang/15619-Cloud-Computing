#!/usr/bin/python

import sys
import os

language='en'
pageex=('Media', 'Special', 'Talk', 'User', 'User_talk', 'Project', 'Project_talk', 'File', 'File_talk', 'MediaWiki', 'MediaWiki_talk', 'Template', 'Template_talk', 'Help', 'Help_talk', 'Category', 'Category_talk', 'Portal', 'Wikipedia', 'Wikipedia_talk')
lowercasech=('q','w','e','r','t','y','u','i','o','p','l','k','j','h','g','f','d','s','a','z','x','c','v','b','n','m')
img=('.jpg','.gif','.png','.JPG','.GIF','.PNG','.txt','.ico')
titleex=('404_error/', 'Main_Page', 'Hypertext_Transfer_Protocol', 'Favicon.ico', 'Search')


filename=os.environ["map_input_file"]
#filename="201306-gz/pagecounts-20130601-000000"
filename=filename[0:filename.find('.')]
info=filename.split("-")
hourdate=info[2]+info[3] #20130601000000

for line in sys.stdin:
    item=line.rstrip('\n').rstrip('\r').split(" ")
    if not item[0].startswith(language):
        continue
    if not item[0].find('.') == -1:
        continue
    if item[1].startswith(pageex):
        continue    
    if item[1].endswith(img):
        continue
    if item[1].startswith(lowercasech):
        continue
    if item[1] in titleex:
        continue
    print item[1]+"\t"+hourdate+item[2]