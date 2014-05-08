# Create raid0
sudo umount /dev/xvdb
sudo mdadm --create /dev/md0 --level=0 --chunk=256 --raid-devices=4 /dev/xvdb /dev/xvdc /dev/xvdd /dev/xvde 
sudo cat /proc/mdstat
sudo mkfs.ext4 /dev/md0


#Mount a volumn
sudo mkdir /storage/raid0
sudo mount /dev/md0 /storage/raid0
cd /storage/raid0

#link mysql server with the mounted point just created
sudo cp -a /home/mysql_backup/* .
sudo chown mysql:mysql /storage/ramblock
sudo service mysql stop

sudo mount --bind /storage/raid0 /var/lib/mysql
sudo service mysql start
sudo cp -R /var/lib/mysql/ /home/mysql_backup/.
