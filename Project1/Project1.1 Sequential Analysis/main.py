import re

filename = 'sample'
totalCounts = 0
counts = 0
regex = "en\s((?!Media:|Special:|Talk:|User:|User_talk:|Project:" \
            "|Project_talk:|File:|File_talk:|MediaWiki:|MediaWiki_talk:" \
            "|Template:|Template_talk:|Help:|Help_talk:|Category:" \
            "|Category_talk:|Portal:|Wikipedia:|Wikipedia_talk:" \
            "|404_error/|Main_Page|Hypertext_Transfer_Protocol" \
            "|Favicon.ico|Search)[A-Z\d]\w+)+" \
            ":(.*)\.((?!jpg|gif|png|JPG|GIF|PNG|txt|ico)\w)+\s\d+\s(\d+)"
rg = re.compile(regex)

def filter(line):
    m = rg.search(line)
    if m:
        print m.group(1),m.group(2),m.group(3),m.group(4)
        global counts
        counts += 1

with open(filename) as fp:


    for line in fp:
        filter(line)
        totalCounts += 1

    print totalCounts
    print counts
