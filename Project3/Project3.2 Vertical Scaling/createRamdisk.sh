# Create RAMDISK
sudo mkdir /storage/tmpfs
sudo mount -t tmpfs -o size=2001M tmpfs /storage/tmpfs
#create the file named ramblock, fill it with NULL:
dd if=/dev/zero of=/storage/tmpfs/ramblock bs=1M count=2000
sudo mkfs.ext4 /storage/tmpfs/ramblock






############################################
#Mount a volumn
sudo mkdir /storage/ramblock
sudo mount -o loop /storage/tmpfs/ramblock /storage/ramblock/
cd /storage/ramblock

#link mysql server with the mounted point just created
sudo cp -a /home/mysql_backup/* .
sudo chown mysql:mysql /storage/ramblock
sudo service mysql stop

sudo mount --bind /storage/ramblock /var/lib/mysql
sudo service mysql start
sudo cp -R /var/lib/mysql/ /home/mysql_backup/.



