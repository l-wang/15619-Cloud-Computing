#!/usr/bin/python

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
import boto.ec2.elb
from boto.ec2.elb import HealthCheck


AWS_ACCESS_KEY = 'AKIAIHXVS6TDDIYJG75Q'
AWS_SECRET_KEY = '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'
CONNECT_REGION = 'us-east-1'
CONNECT_AVAILABILITY_ZONE = 'us-east-1b'
AMI = 'ami-69e3d500'
KEY_NAME = 'Project2_1'
INSTANCE_TYPE = 'm1.small'

script_one='./apache_bench.sh sample.jpg 100000 100 '
# script_one='./apache_bench.sh sample.jpg 100 10 '
script_two=' logfile > '
file_name = 'out'


#boto.config.add_section('Credentials')
boto.config.set('Credentials',  'aws_access_key_id', AWS_ACCESS_KEY)
boto.config.set('Credentials', 'aws_secret_access_key', AWS_SECRET_KEY)

##################### ec2 instance
instance_ids = []
instance_cnt = 0
throughput = 0

conn = boto.ec2.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
security_groups=conn.get_all_security_groups()
print security_groups
security_group=security_groups[2]

print security_group


##################### elb
boto.ec2
regions = boto.ec2.elb.regions()

print regions
elb = boto.ec2.elb.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)

# conn = boto.ec2.connect_to_region("us-east-1")
list = elb.get_all_load_balancers()
print list

hc = HealthCheck(
    interval=15,
    target='HTTP:8080/upload'
)
 
 
zones = [CONNECT_AVAILABILITY_ZONE]
ports = [(80, 80, 'http'), (8080, 8080, 'http')]
lb = elb.create_load_balancer('my-lb', zones, ports)
lb.configure_health_check(hc)
 
print lb.dns_name



while throughput <=2000:
    reservation=conn.run_instances(AMI,key_name=KEY_NAME,instance_type=INSTANCE_TYPE,placement=CONNECT_AVAILABILITY_ZONE,security_groups=[security_group])
    instance_cnt
    print reservation
    instance = reservation.instances[0]
    instance_id = instance.id
    print instance_id
    
    instance_ids.append(instance_id)
    sleep(180)
    
    lb.register_instances([instance_id])
    sleep(120)
    
#     reservations = conn.get_all_instances([instance_id])
#      
#     instance_dns = [ i.public_dns_name for r in reservations for i in r.instances ]
#     instance_dns = instance_dns[0].strip()
#     print instance_dns
#     
#     instance_dns = 'localhost'
    
    real_file = file_name + str(instance_cnt)
    cmd = script_one + lb.dns_name + script_two + real_file
    print cmd
    
    os.system(cmd)
    
    ### Parse file
    
    for line in open(real_file,'r'):
        if line.startswith('Requests per second:'):
            ss = line.split(':')
            print "list1:"
            print ss
            sub = ss[1].strip().split(' ')
            print "list2:"
            throughput = float(sub[0])
            break
    
    print 'throughput', str(throughput)

 

conn.terminate_instances(instance_ids=instance_ids)
lb.delete()
print 'total instances:', instance_cnt
