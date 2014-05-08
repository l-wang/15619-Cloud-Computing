# Running sysbench

cd ~/sysbench-0.5/sysbench
export RUN_NAME=myRun3
export MYSQL_SERVER=ec2-23-22-12-151.compute-1.amazonaws.com
sudo ./sysbench --test=tests/db/oltp.lua --mysql-host=$MYSQL_SERVER --mysql-user=sysbench --mysql-password=project3 --oltp-table-size=5000000 --num-threads=16 --max-requests=0 --max-time=30 --report-interval=5 --oltp-read-only=on run | tee $RUN_NAME.out



