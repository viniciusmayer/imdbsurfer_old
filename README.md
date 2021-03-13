# project setup

## python3 setup
```
sudo apt-get install python3
```

## git setup 
```
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git
```

## postgresql database setup
### install
```
sudo nano /etc/apt/sources.list.d/pgdg.list
	deb http://apt.postgresql.org/pub/repos/apt/ artful-pgdg main
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
sudo -u postgres psql
	\conninfo
	\q
```
### configure
```
sudo nano /etc/postgresql/9.6/main/pg_hba.conf
sudo nano /etc/postgresql/9.6/main/postgresql.conf
sudo service postgresql restart
sudo su - postgres
psql
\password
	p0stgr3s
sudo -u postgres createuser --interactive
	imdbsurfer
	n
	n
	n
sudo adduser imdbsurfer
	1mdbsurf3r
	1mdbsurf3r
	IMDb Surfer Database User
	[enter]
	[enter]
	[enter]
	[enter]
	Y
sudo -u postgres createdb imdbsurfer --owner=imdbsurfer
sudo -u imdbsurfer psql
	\conninfo
	\q
```

### system setup
```
sudo adduser postgres
sudo passwd postgres
	p0stgr3s
sudo adduser imdbsurfer
sudo passwd imdbsurfer
	1mdbsurf3r
```

# pip setup
```
wget https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py
./get-pip.py
```

## app setup
```
git clone https://github.com/viniciusmayer/imdbsurfer.git
virtualenv -p python3 imdbsurfer
cd imdbsurfer
source bin/activate
pip install scrapy
pip install psycopg2-binary
```

## additional steps
```
git config --global user.email "viniciusmayer@gmail.com"
git config --global user.email "Vinicius Mayer"
```

## new configuration
docker network create --driver bridge postgres-network
docker run --name postgres-database -p 5432:5432 --network=postgres-network -e POSTGRES_PASSWORD=p0stgr3s -d postgres
docker run --name postgres-admin --network=postgres-network -p 15432:80 -e "PGADMIN_DEFAULT_EMAIL=viniciusmayer@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=pg4dm1n" -d dpage/pgadmin4