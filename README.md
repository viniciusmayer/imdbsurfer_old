# project setup

## python setup
```
sudo apt-get install python3
```

## git setup 
```
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git
```

## database setup
```
sudo nano /etc/apt/sources.list.d/pgdg.list
> deb http://apt.postgresql.org/pub/repos/apt/ artful-pgdg main
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
sudo -u postgres psql
	\conninfo
	\q
sudo -u postgres createuser --interactive
	imdbsurfer
	n
	n
	n
sudo -u postgres createdb imdbsurfer
sudo adduser imdbsurfer
	1mdbsurf3r
	1mdbsurf3r
	IMDb Surfer Database User
	[enter]
	[enter]
	[enter]
	[enter]
	Y
sudo -u imdbsurfer psql
	\conninfo
	\q
```

## app setup
```
git clone https://github.com/viniciusmayer/imdbsurfer.git
virtualenv -p python3 imdbsurfer
cd imdbsurfer
source bin/activate
pip install scrapy
pip install psycopg2
```

## additional steps
```
git config --global user.email "viniciusmayer@gmail.com"
git config --global user.email "Vinicius Mayer"
```