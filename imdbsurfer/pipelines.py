# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#{
#    "index": "5",
#    "year": "1999",
#    "link": "/title/tt0133093",
#    "name": "The Matrix",
#    "genres": [
#        "Action",
#        "Sci-Fi"
#    ],
#    "minutes": "136",
#    "rate": "8.7",
#    "metascore": "73",
#    "directors": [
#        "Lana Wachowski",
#        "Lilly Wachowski"
#    ],
#    "stars": [
#        "Keanu Reeves",
#        "Laurence Fishburne",
#        "Carrie-Anne Moss",
#        "Hugo Weaving"
#    ],
#    "votes": "1,314,055"
#},

import psycopg2, itertools

selectUserByEmail = 'select id from auth_user where email = %s'
email = 'viniciusmayer@gmail.com'

selectGenreByName = 'select id from imdbsurfer_genre where name = %s'
insertIntoGenre = 'INSERT INTO imdbsurfer_genre(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectRoleByName = 'SELECT id FROM imdbsurfer_role where name = %s'
insertIntoRole = 'INSERT INTO imdbsurfer_role(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectArtistByName = 'SELECT id FROM imdbsurfer_artist where name = %s'
insertIntoArtist = 'INSERT INTO imdbsurfer_artist(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectArtistRole = 'SELECT id FROM imdbsurfer_artistrole where artist_id in ({0}) and role_id in ({1})'.format(selectArtistByName, selectRoleByName)
insertIntoArtistRole = 'INSERT INTO imdbsurfer_artistrole(dh_create, dh_update, artist_id, role_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectArtistByName, selectRoleByName, selectUserByEmail, selectUserByEmail)

selectMovie = 'SELECT id FROM imdbsurfer_movie where name = %s and year = %s and link = %s and minutes = %s' 
insertIntoMovie = \
    'INSERT INTO imdbsurfer_movie(name, year, index, rate, votes, link, metascore, minutes, watch, watched, dh_create, dh_update, user_create_id, user_update_id)'\
    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, False, False, now(), now(), ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

roles = ['Director', 'Star']
psycopg_connect = 'dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''viniciusmayer'''

class CleanPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        item['index'] = self.index(item['index'])
        item['votes'] = self.votes(item['votes'])
        item['year'] = self.year(item['year'])
        item['minutes'] = self.minutes(item['minutes'])
        item['link'] = self.link(item['link'])
        item['genres'] = self.genres(item['genres'])
        item['name'] = self.extractAndClean(item['name'])
        item['rate'] = self.extractAndClean(item['rate'])
        item['metascore'] = self.extractAndClean(item['metascore'])
        c = self.artists(item['artistsa'], item['artistsb'])
        item['directors'] = self.directors(c)
        item['stars'] = self.stars(c)
        return item

    def artists(self, a, b):
        _a = []
        for i in a:
            _a.append(self.clean(i))
        _b = []
        for i in b:
            _b.append(self.clean(i))
        _b.remove('')
        return list(itertools.chain.from_iterable(zip(_b,_a)))
    
    def directors(self, value):
        _value = value[1:value.index('Stars:')]
        return [v for v in _value if v != ',']
    
    def stars(self, value):
        _value = value[value.index('Stars:') + 1:len(value)]
        return [v for v in _value if v != ',']

    def genres(self, value):
        _value = []
        for i in value[0].split(","):
            _value.append(self.clean(i))
        return _value

    def link(self, value):
        return value[0][:value[0].find('?') - 1]

    def minutes(self, value):
        return self.clean(value[0].split()[0])

    def year(self, value):
        return self.extractAndClean(value).replace('(', '').replace(')', '')

    def votes(self, value):
        return self.extractAndClean(value, 1).replace(',', '')

    def index(self, value):
        return self.extractAndClean(value).replace('.', '')
    
    def extractAndClean(self, value, pos=0):
        if value is not None and len(value) > pos:
            return self.clean(value[pos])
        return None
    
    def clean(self, value):
        if value is not None:
            return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
        return None

class GenrePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for genre in item['genres']:
            try:
                self.cursor.execute(selectGenreByName, [genre])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoGenre, [genre, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)
                
        return item
    
class RolePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for role in roles:
            try:
                self.cursor.execute(selectRoleByName, [role])
                if self.cursor.rowcount == 0:
                    self.cursor.execute(insertIntoRole, [role, email, email])
                    self.cursor.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)                            

        return item

class Artist_ArtistRolePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for director in item['directors']:
            try:
                self.cursor.execute(selectArtistByName, [director])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist, [director, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)

            try:
                self.cursor.execute(selectArtistRole, [director, roles[0]])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [director, roles[0], email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)

        for star in item['stars']:
            try:
                self.cursor.execute(selectArtistByName, [star])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist, [star, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)

            try:
                self.cursor.execute(selectArtistRole, [star, roles[1]])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [star, roles[1], email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### ERROR: ')
                print(e)

        return item

class MoviePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        name = item['name']
        year = item['year']
        index = item['index']
        rate = item['rate']
        votes = item['votes']
        link = item['link']
        metascore = item['metascore']
        minutes = item['minutes']
        
        try:
            self.cursor.execute(selectMovie, [name, year, link, minutes])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoMovie, [name, year, index, rate, votes, link, metascore, minutes, email, email])
                self.connection.commit()
        except Exception as e:
            print('##### ERROR: ')
            print(e)
            print(self.cursor.mogrify(insertIntoMovie, [name, year, index, rate, votes, link, metascore, minutes, email, email]))
            
        return item