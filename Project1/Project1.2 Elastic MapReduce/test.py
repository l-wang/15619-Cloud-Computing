
filename="201306-gz/pagecounts-20130601-000000"
filename=filename[0:filename.find('.')]
info=filename.split("-")
hourdate=info[2]+info[3] #20130601000000

print hourdate

line = "zu File:Location_Guinea_Bissau_AU_Africa.svg 1 9519"
item=line.rstrip('\n').rstrip('\r').split(" ")
print item[0]
print item[1]
print item[2]

info = "201306010000001"
date=info[0:8]
hour=info[8:14]
views=info[14:]
print date
print hour
print views