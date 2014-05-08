#!/usr/bin/python

import sys
import datetime
import boto
import boto.ec2.connection
import boto.route53.connection
import boto.route53.hostedzone
import boto.route53.record
import boto.route53.exception
import boto.ec2.autoscale
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import ScalingPolicy
import boto.ec2.cloudwatch
from boto.ec2.cloudwatch import MetricAlarm
from time import sleep
import os
from boto.ec2.connection import EC2Connection
import boto.ec2.elb
from boto.ec2.elb import HealthCheck


AWS_ACCESS_KEY = 'AKIAIHXVS6TDDIYJG75Q'
AWS_SECRET_KEY = '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'
CONNECT_REGION = 'us-east-1'
CONNECT_AVAILABILITY_ZONE = 'us-east-1b'
AMI = 'ami-99e2d4f0'
KEY_NAME = 'Project2_1'
INSTANCE_TYPE = 'm1.small'

script_one='./apache_bench.sh sample.jpg 100000 100 '
# script_one='./apache_bench.sh sample.jpg 100 10 '
script_two=' logfile > '
file_name = 'out'


MIN_SIZE = 2
MAX_SIZE = 5
ARN = 'arn:aws:sns:us-east-1:782142299950:demo'


ASG_NAME = 'my_asg_group13'
LB_NAME = 'mylb13'
CONFIG_NAME = '15619-launch_confi13'

boto.config.add_section('Credentials')
boto.config.set('Credentials',  'aws_access_key_id', AWS_ACCESS_KEY)
boto.config.set('Credentials', 'aws_secret_access_key', AWS_SECRET_KEY)

##################### ec2 instance
instance_ids = []
instance_cnt = 0
throughput = 0

ec2_conn = boto.ec2.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
security_groups=ec2_conn.get_all_security_groups()
print security_groups
security_group=security_groups[2]

print security_group


##################### elb_conn
boto.ec2
regions = boto.ec2.elb.regions()

print regions
elb_conn = boto.ec2.elb.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)

# ec2_conn = boto.ec2.connect_to_region("us-east-1")
list = elb_conn.get_all_load_balancers()
print list

hc = HealthCheck(
    interval=240,
    target='HTTP:8080/upload'
)
 
 
zones = [CONNECT_AVAILABILITY_ZONE]
ports = [(80, 80, 'http'), (8080, 8080, 'http')]
lb = elb_conn.create_load_balancer(LB_NAME, zones, ports)





##################### autoscale group
asg_conn = boto.ec2.autoscale.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)

launch_config = LaunchConfiguration(name=CONFIG_NAME, image_id=AMI, key_name=KEY_NAME, security_groups=[security_group], instance_type=INSTANCE_TYPE, instance_monitoring=True)
asg_conn.create_launch_configuration(launch_config)

asg = AutoScalingGroup(group_name=ASG_NAME, load_balancers=[LB_NAME],
                       availability_zones=[CONNECT_AVAILABILITY_ZONE],
                       launch_config=launch_config, min_size=MIN_SIZE, max_size=MAX_SIZE, connection=asg_conn)

asg_conn.create_auto_scaling_group(asg)


scale_up_policy = ScalingPolicy(
            name='scale_up', adjustment_type='ChangeInCapacity',
            as_name=ASG_NAME, scaling_adjustment=1, cooldown=300)

scale_down_policy = ScalingPolicy(
            name='scale_down', adjustment_type='ChangeInCapacity',
            as_name=ASG_NAME, scaling_adjustment=-1, cooldown=300)


asg_conn.create_scaling_policy(scale_up_policy)
asg_conn.create_scaling_policy(scale_down_policy)





##################### cloud watch
cw_conn = boto.ec2.cloudwatch.connect_to_region(CONNECT_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
alarm_dimensions = {"AutoScalingGroupName": ASG_NAME}

scale_up_policy = asg_conn.get_all_policies(
    as_group=ASG_NAME, policy_names=['scale_up'])[0]
    
scale_down_policy = asg_conn.get_all_policies(
    as_group=ASG_NAME, policy_names=['scale_down'])[0]
    
scale_up_alarm = MetricAlarm(
            name='scale_up_on_cpu', namespace='AWS/EC2',
            metric='CPUUtilization', statistic='Average',
            comparison='>', threshold='80',
            period='300', evaluation_periods=1,
            alarm_actions=[scale_up_policy.policy_arn,ARN],
            dimensions=alarm_dimensions)

scale_down_alarm = MetricAlarm(
            name='scale_down_on_cpu', namespace='AWS/EC2',
            metric='CPUUtilization', statistic='Average',
            comparison='<', threshold='20',
            period='300', evaluation_periods=1,
            alarm_actions=[scale_down_policy.policy_arn,ARN],
            dimensions=alarm_dimensions)

cw_conn.create_alarm(scale_up_alarm)
cw_conn.create_alarm(scale_down_alarm)


sleep(120)
lb.configure_health_check(hc)
 
print lb.dns_name

print "done"
 

# lb.delete()
# print 'total instances:', instance_cnt
