# Create ebs
sudo parted /dev/xvdf mklabel gpt
sudo parted /dev/xvdf mkpart db ext4 0% 8G
sudo mkfs.ext4 /dev/xvdf1


#Mount a volumn
sudo mkdir /storage/ebs0
sudo mount /dev/xvdd1 /storage/ebs0
cd /storage/ebs0

#link mysql server with the mounted point just created
sudo cp -a /home/mysql_backup/* .
sudo chown mysql:mysql /storage/ebs0 
sudo service mysql stop

sudo mount --bind /storage/ebs0 /var/lib/mysql
sudo service mysql start
sudo cp -R /var/lib/mysql/ /home/mysql_backup/.

