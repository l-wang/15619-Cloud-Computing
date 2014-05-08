# Create eph0
sudo umount /dev/xvdb
sudo parted /dev/xvdb mklabel gpt
sudo parted /dev/xvdb mkpart db ext4 0% 10G
sudo mkfs.ext4 /dev/xvdb1


#Mount a volumn
sudo mkdir /storage/eph0
sudo mount /dev/xvdb1 /storage/eph0
cd /storage/eph0

#link mysql server with the mounted point just created
sudo cp -a /home/mysql_backup/* .
sudo chown mysql:mysql /storage/eph0 
sudo service mysql stop

sudo mount --bind /storage/eph0 /var/lib/mysql
sudo service mysql start
sudo cp -R /var/lib/mysql/ /home/mysql_backup/.

















