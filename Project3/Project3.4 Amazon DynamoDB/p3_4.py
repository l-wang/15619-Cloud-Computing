#!/usr/bin/python

import boto
from boto.dynamodb.condition import *
import csv

AWS_ACCESS_KEY = 'AKIAIHXVS6TDDIYJG75Q'
AWS_SECRET_KEY = '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'
CSV_FILE = 'caltech-256.csv'

conn = boto.connect_dynamodb(AWS_ACCESS_KEY, AWS_SECRET_KEY)

print conn
print conn.list_tables()
table = conn.get_table('Caltech256')

print table

file = open(CSV_FILE, "rb")
reader = csv.reader(file)

cnt = 0
item_data = {
        'Body': 'http://url_to_lolcat.gif',
        'SentBy': 'User A',
        'ReceivedTime': '12/9/2011 11:36:03 PM',
    }
for row in reader:
#     print row
#     for col in row:
#         print col + ":"
    if cnt != 0:
        print row[0] + ":" + row[1] + ":" + row[2]
        item = table.new_item(
            # Our hash key is 'forum'
            hash_key=row[0],
            # Our range key is 'subject'
            range_key=int(row[1]),
            # This has the
            attrs={'S3URL':row[2]}
        )
        print item
        item.put()
    cnt += 1
#     if cnt==5:
#         break
    

file.close
