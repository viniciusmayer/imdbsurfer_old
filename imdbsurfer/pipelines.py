# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#{
#    "genres": [
#        "Action",
#        "Sci-Fi"
#    ],
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

selectMovieGenre = 'SELECT id FROM imdbsurfer_moviegenre where genre_id = ({0}) and movie_id = ({1})'.format(selectGenreByName, selectMovie)
insertIntoMovieGenre = 'INSERT INTO imdbsurfer_moviegenre(dh_create, dh_update, genre_id, movie_id, user_create_id, user_update_id)'\
    'VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectGenreByName, selectMovie, selectUserByEmail, selectUserByEmail)

selectMovieArtistRole = 'SELECT id FROM imdbsurfer_movieartistrole where "artistRole_id" = ({0}) and movie_id = ({1})'.format(selectArtistRole, selectMovie)
insertIntoMovieArtistRole = 'INSERT INTO imdbsurfer_movieartistrole(dh_create, dh_update, "artistRole_id", movie_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectArtistRole, selectMovie, selectUserByEmail, selectUserByEmail)

roles = ['Director', 'Star']
psycopg_connect = 'dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''viniciusmayer'''

class CleanPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        item['index'] = self.cleanInteger(item['index'][0])
        item['votes'] = self.cleanInteger(item['votes'][1])
        item['year'] = self.cleanInteger(item['year'][0])
        item['minutes'] = self.cleanInteger(item['minutes'][0])
        item['link'] = self.cleanLink(item['link'][0])
        item['genres'] = self.cleanGenres(item['genres'][0])
        item['name'] = self.cleanString(item['name'][0])
        item['rate'] = self.cleanString(item['rate'][0])
        item['metascore'] = self.cleanInteger(item['metascore'][0]) if len(item['metascore']) > 0 else None
        c = self.cleanArtists(item['artistsa'], item['artistsb'])
        item['directors'] = self.cleanDirectors(c)
        item['stars'] = self.cleanStars(c)
        return item

    def cleanArtists(self, a, b):
        _a = []
        for i in a:
            _a.append(self.cleanString(i))
        _b = []
        for i in b:
            _b.append(self.cleanString(i))
        _b.remove('')
        return list(itertools.chain.from_iterable(zip(_b,_a)))
    
    def cleanDirectors(self, value):
        _value = value[1:value.index('Stars:')]
        return [v for v in _value if v != ',']
    
    def cleanStars(self, value):
        _value = value[value.index('Stars:') + 1:len(value)]
        return [v for v in _value if v != ',']

    def cleanGenres(self, value):
        _value = []
        for i in value.split(","):
            _value.append(self.cleanString(i))
        return _value

    def cleanLink(self, value):
        return 'http://www.imdb.com{0}'.format(value[:value.find('?') - 1])

    def cleanInteger(self, value):
        return ''.join(i for i in value if i.isdigit())
    
    def cleanString(self, value):
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
                print('##### GenrePipeline.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoGenre, [genre, email, email]))
                
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
                    self.connection.commit()
            except Exception as e:
                print('##### RolePipeline.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoRole, [role, email, email]))

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
                print('##### Artist_ArtistRolePipeline.1.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoArtist, [director, email, email]))

            try:
                self.cursor.execute(selectArtistRole, [director, roles[0]])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [director, roles[0], email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### Artist_ArtistRolePipeline.2.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoArtistRole, [director, roles[0], email, email]))

        for star in item['stars']:
            try:
                self.cursor.execute(selectArtistByName, [star])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist, [star, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### Artist_ArtistRolePipeline.3.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoArtist, [star, email, email]))

            try:
                self.cursor.execute(selectArtistRole, [star, roles[1]])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [star, roles[1], email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### Artist_ArtistRolePipeline.4.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoArtistRole, [star, roles[1], email, email]))

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
            print('##### MoviePipeline.1.ERROR: ')
            print(e)
            print(self.cursor.mogrify(insertIntoMovie, [name, year, index, rate, votes, link, metascore, minutes, email, email]))
        
        genres = item['genres']
        for genre in genres:
            try:
                self.cursor.execute(selectMovieGenre, [genre, name, year, link, minutes])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoMovieGenre, [genre, name, year, link, minutes, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### MoviePipeline.2.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoMovieGenre, [genre, name, year, link, minutes, email, email]))
        
        directors = item['directors']
        for director in directors:
            try:
                self.cursor.execute(selectMovieArtistRole, [director, roles[0], name, year, link, minutes])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoMovieArtistRole, [director, roles[0], name, year, link, minutes, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### MoviePipeline.3.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoMovieArtistRole, [director, roles[0], name, year, link, minutes, email, email]))
        
        stars = item['stars']
        for star in stars:
            try:
                self.cursor.execute(selectMovieArtistRole, [star, roles[1], name, year, link, minutes])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoMovieArtistRole, [star, roles[1], name, year, link, minutes, email, email])
                    self.connection.commit()
            except Exception as e:
                print('##### MoviePipeline.4.ERROR: ')
                print(e)
                print(self.cursor.mogrify(insertIntoMovieArtistRole, [star, roles[1], name, year, link, minutes, email, email]))

        return item