# python3
# compile from source
# ref: http://www.extellisys.com/articles/python-on-debian-wheezy
apt-get install build-essential
apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev
apt-get install libdb5.1-dev libgdbm-dev libsqlite3-dev libssl-dev
apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
cd /tmp
# ---- download python source from main website
tar -zxf /path/to/your/Python-3.<VERSION>.tgz
cd Python-<VERSION>
./configure --prefix=/usr/local/opt/python-<VERSION>
make
make install
cd /tmp
rm -rf Python-<VERSION>
ln -s /usr/local/opt/python-<VERSION>/bin/python /usr/bin/python3

# postgres
# http://www.postgresql.org/download/linux/debian/
# https://wiki.postgresql.org/wiki/Apt
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc |  apt-key add -
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-9.4
pg_createcluster 9.4 main --start

# redis
echo "deb-src http://packages.dotdeb.org wheezy all" >> /etc/apt/sources.list.d/dotdeb.list
wget http://www.dotdeb.org/dotdeb.gpg
apt-key add - < dotdeb.gpg
apt-get install redis-server

#  nginx
apt-get install nginx-full

# uwsgi
pip3 install uwsgi
#copy uwsgi.upstart as /etc/init.d/uwsgi
# edit /etc/init.d/uwsgi and point to correct pip-installed binary by searching for <VERSION>
# and replace it with the python installed


# uwsgi
# install both from pip and debian-specific
pip3 install uwsgi
# we need the debian-specific to get premade init.d scripts
apt-get install uwsgi
# edit /etc/init.d/uwsgi and point to correct pip-installed binary by searching for `DAEMON=`
# and replace it with the python installed


# copy nginx and uwsgi sample files
cp env/uwsgi.ini-sample /etc/uwsgi/apps-enabled/live.ini
cp env/nginx.conf-sample /etc/nginx/sites-enabled/live.conf
