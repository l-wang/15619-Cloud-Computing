#!/usr/bin/python

special = ['Media', 'Special', 'Talk', 'User', 'User_talk',
           'Project', 'Project_talk', 'File', 'File_talk',
           'MediaWiki', 'MediaWiki_talk', 'Template',
           'Template_talk', 'Help', 'Help_talk', 'Category',
           'Category_talk', 'Portal', 'Wikipedia', 'Wikipedia_talk']

extension = ['.jpg', '.gif', '.png', '.JPG', '.GIF', '.PNG', '.txt', '.ico']

boilerplate = ['404_error/', 'Main_Page', 'Hypertext_Transfer_Protocol', 'Favicon.ico', 'Search']

ins = open( "pagecounts-20130601-000000", "r" )
array = []
mydict = dict()
total = 0
total_views = 0

for line in ins:
    total += 1
    line = line.strip()
    if line.__len__() == 0:
        continue

    split_result = line.split(' ')
    first = split_result[0]
    article = split_result[1]

    pageviews = split_result[2]
    total_views += int(pageviews)

    # 1) Skip all page not start with 'en'
    if not first == 'en':
        continue

    # Skip pages containing special word
    hit = False
    for word in special:
        if article.startswith(word):
            hit = True
            break
    if hit:
        continue

    # Check lower case
    if article[0].islower():
        continue

    # Check extension
    hit = False
    for word in extension:
        if article.endswith(word):
            hit = True
            break
    if hit:
        continue

    # Check boilerplate
    hit = False
    for word in boilerplate:
        if word == article:
            hit = True
            break
    if hit:
        continue


    # print article, '    ', pageviews

    array.append( line )
    mydict[article] = int(pageviews)

# print mydict
# print sorted(mydict, key=mydict.get, reverse=True)
for w in sorted(mydict, key=mydict.get, reverse=True):
	print w, mydict[w]

print 'total:', total
print 'total_views:', total_views
print len(array)
