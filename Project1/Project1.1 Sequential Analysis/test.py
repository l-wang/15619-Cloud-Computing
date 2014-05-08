def match():
	import re
	fileRead=open("test.txt", "r")
	line=fileRead.readline()
	outList=[]
	i=0
	j=0
	pageview=0
	while(line!=''):
		j=j+1
		strList=line.split(' ')
		pageview=pageview+int(strList[2])
		if(filter(line, strList)==True):
			outList.append(strList)
			i=i+1
		line=fileRead.readline()
	fileRead.close()
	# outList.sort(key=lambda tup: tup[2])
	# value=outList[-1]
	# print (value[0]+'\t'+value[1]+'\t'+value[2]+'\t'+value[3])
	# print (value[1]+'\t'+value[2])
	print('before '+str(j))
	print ('total number '+str(i))
	print ('total pageview '+ str(pageview))

def filter_step1(line):
	import re
	if(line[0] == 'en'):
		return True
	return False

def filter_step2(line):
	import re
	list=['Media', 'Special', 'Talk', 'User', 'User_talk', 'Project', 'Project_talk', 'File', 'File_talk', 'MediaWiki', 'MediaWiki_talk', 'Template', 'Template_talk', 'Help', 'Help_talk', 'Category', 'Category_talk', 'Portal', 'Wikipedia', 'Wikipedia_talk']
	#list=['Media', 'Special', 'Talk', 'User', 'Project', 'File', 'MediaWiki', 'Template', 'Help', 'Category', 'Portal', 'Wikipedia']
	for value in list:
		if line.startswith(value):
			return False
	return True

def filter_step3(line):
	import re
	list=['.jpg', '.gif', '.png', '.JPG', '.GIF', '.PNG', '.txt', '.ico']
	for value in list:
		if(line.endswith(value)):
			return False
	return True

def filter_step4(line):
	import re
	list=['404_error/', 'Main_Page', 'Hypertext_Transfer_Protocol', 'Favicon.ico', 'Search']
	for value in list:
		if(value==line):
			return False
	else:
		return True

def filter(line, strList):
	return(filter_step1(strList[0]) and filter_step2(strList[1]) and filter_step3(strList[1]))






match()
