
# backup current Db and then restore a dump

./backup.sh
echo "Restore vulnerablecode dump from: $1"
sudo -u postgres dropdb vulnerablecode
sudo -u postgres createdb --encoding=utf-8 --owner=vulnerablecode vulnerablecode
sudo su - postgres bunzip2 -c | $1


