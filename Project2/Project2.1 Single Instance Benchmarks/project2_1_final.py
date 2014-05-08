

import sys
import datetime
import boto
import boto.ec2.connection
import boto.route53.connection
import boto.route53.hostedzone
import boto.route53.record
import boto.route53.exception
from time import sleep
import os
from boto.ec2.connection import EC2Connection


AWS_ACCESS_KEY = 'AKIAIHXVS6TDDIYJG75Q'
AWS_SECRET_KEY = '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'
new_instance_type='m1.small'
instances=('m1.small','m1.medium','m1.large')
ami='ami-69e3d500'
script_one='./apache_bench.sh sample.jpg 100000 100 '
script_two=' logfile > out'
max_time=10
key_name='Project2_1'

instance_id = ''
instance_dns = ''
file_name = 'out'






cnt = 0

while cnt < 10:
	# old_stdout = sys.stdout
	# log_file = open(file_name + "-CW-" + str(cnt),"w")
	# sys.stdout = log_file
	printlogfilename = file_name + "-CW-" + str(cnt)
	f = open(printlogfilename,'w')
	print cnt
	f.write('cnt:'+str(cnt)+'\n')

	conn = boto.ec2.connect_to_region('us-east-1',aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
	security_groups=conn.get_all_security_groups()
	security_group=security_groups[1]
	reservation=conn.run_instances(ami,key_name=key_name,instance_type=new_instance_type,security_groups=[security_group])
	print reservation
	instance = reservation.instances[0]
	instance_id = instance.id
	print instance_id
	print instance.public_dns_name
	f.write(instance_id+'\n')
	f.write(instance.public_dns_name+'\n')

	print "================"
	instance_list = [instance_id]
	# list = ['i-dbbcd6f5']

	sleep(120)
	reservations = conn.get_all_instances(instance_list)

	instance_dns = [ i.public_dns_name for r in reservations for i in r.instances ]
	instance_dns = instance_dns[0].strip()
	print instance_dns
	f.write(instance_dns+'\n')
	cmd = script_one + instance_dns + script_two + file_name + str(cnt)
	print cmd
	f.write(cmd+'\n')


	# Cloud watch
	class InstanceDimension(dict):
	    def __init__(self, name, value):
	        self[name] = value

	c = boto.connect_cloudwatch(AWS_ACCESS_KEY, AWS_SECRET_KEY)


	# cmd = './apache_bench.sh sample.jpg 100000 100 ec2-50-16-20-21.compute-1.amazonaws.com logfile > outout1'
	os.system(cmd)


	end   = datetime.datetime.now()
	start = end - datetime.timedelta(hours=2)
	stats = c.get_metric_statistics(
	    60, 
	    start, 
	    end, 
	    'CPUUtilization', 
	    'AWS/EC2', 
	    'Average', 
	    InstanceDimension("InstanceId", instance_id)
	)

	
	print stats
	f.write(str(stats))

	conn.terminate_instances(instance_ids=[instance_id])

	# sys.stdout = old_stdout
	# log_file.close()
	f.close()

	cnt += 1




