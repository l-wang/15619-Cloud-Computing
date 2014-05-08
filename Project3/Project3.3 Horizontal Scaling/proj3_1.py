#!/usr/bin/python
import os
import re
import sys
import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.cloudwatch
from boto.ec2.elb import HealthCheck
import time


def query_cnts():
    stream = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Queries\'\"").read()
    index_stream = stream.find("Queries")
    number_stream = stream[index_stream+7:]
    print(number_stream)
    query = (int)(number_stream)-3
    return query

def get_db_time():
    stream = os.popen("/usr/bin/mysql -u root -pdb15319root --execute=\"show status like \'Uptime\'\"").read()
    index = stream.find("Uptime")
    number_stream = stream[index+6:]
    time_get = int(number_stream)
    return time_get

def main(argv):
	stream = os.popen("/usr/bin/wget -q -O - http://169.254.169.254/latest/meta-data/instance-id").read()
    print stream
    instanceid = stream[2:]

    elb = boto.ec2.cloudwatch.connect_to_region('us-east-1', aws_access_key_id='AKIAIHXVS6TDDIYJG75Q', aws_secret_access_key='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')
    begin_query = query_cnts()
    begin_time = get_db_time()
    begin_query = begin_query + 6
    time.sleep(60)

    while(True):
        query_curr = query_cnts()
        time_curr = get_db_time()
        ratio_query_query = (query_curr-begin_query)*12/(time_curr-begin_time)/156.2/16
        ratio_query = 0
        elb.put_metric_data("demo/TPS","TPS",ratio_query,'','Percent',dict(InstanceID=instid),'')
        begin_query = query_curr+6
        begin_time = time_curr
        time.sleep(60)

if __name__=="__main__":
    main(sys.argv)
