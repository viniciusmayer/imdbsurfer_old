# -*- coding: utf-8 -*-
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

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

selectMovieByLink = 'SELECT id FROM imdbsurfer_movie where link = %s' 
insertIntoMovie = \
    'INSERT INTO imdbsurfer_movie(name, year, rate, votes, link, metascore, minutes, watch, watched, dh_create, dh_update, user_create_id, user_update_id)'\
    ' VALUES (%s, %s, %s, %s, %s, %s, %s, False, False, now(), now(), ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)
updateMovie = 'UPDATE imdbsurfer_movie SET dh_update=now(), rate=%s, votes=%s, metascore=%s, user_update_id=({0}) WHERE link=%s'.format(selectUserByEmail)

selectMovieGenre = 'SELECT id FROM imdbsurfer_moviegenre where genre_id = ({0}) and movie_id = ({1})'.format(selectGenreByName, selectMovieByLink)
insertIntoMovieGenre = 'INSERT INTO imdbsurfer_moviegenre(index, dh_create, dh_update, genre_id, movie_id, user_create_id, user_update_id)'\
    'VALUES (%s, now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectGenreByName, selectMovieByLink, selectUserByEmail, selectUserByEmail)
updateMovieGenre = 'UPDATE imdbsurfer_moviegenre SET dh_update=now(), index=%s, user_update_id=({0})'\
    ' WHERE genre_id=({1}) and movie_id=({2})'.format(selectUserByEmail, selectGenreByName, selectMovieByLink)

selectMovieArtistRole = 'SELECT id FROM imdbsurfer_movieartistrole where "artistRole_id" = ({0}) and movie_id = ({1})'.format(selectArtistRole, selectMovieByLink)
insertIntoMovieArtistRole = 'INSERT INTO imdbsurfer_movieartistrole(dh_create, dh_update, "artistRole_id", movie_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectArtistRole, selectMovieByLink, selectUserByEmail, selectUserByEmail)

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
        item['genre'] = self.cleanGenre(item['genre'])
        return item

    def cleanGenre(self, value):
        return value[value.find('genres') + 7:value.find('num_votes') - 1]

    def cleanArtists(self, a, b):
        _a = []
        for i in a:
            _a.append(self.cleanString(i))
        _b = []
        for i in b:
            _b.append(self.cleanString(i))
        _b.remove('')
        return list(itertools.chain.from_iterable(zip(_b, _a)))
    
    def cleanDirectors(self, value):
        end = None
        try:
            end = value.index('Stars:') 
        except ValueError:
            pass
        if (end is None):
            try:
                end = value.index('Star:')
            except ValueError:
                pass
        _value = value[1:end]
        return [v for v in _value if v != ',']
    
    def cleanStars(self, value):
        begin = None
        try:
            begin = value.index('Stars:') 
        except ValueError:
            pass
        if (begin is None):
            try:
                begin = value.index('Star:')
            except ValueError:
                pass
        if (begin is None):
            return None
        _value = value[begin + 1:len(value)]
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
        if (value is not None):
            return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
        return None

class GenrePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for genre in item['genres']:
            self.cursor.execute(selectGenreByName, [genre])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoGenre, [genre, email, email])
                self.connection.commit()
                
        return item
    
class RolePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for role in roles:
            self.cursor.execute(selectRoleByName, [role])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoRole, [role, email, email])
                self.connection.commit()

        return item

class ArtistPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for director in item['directors']:
            self.cursor.execute(selectArtistByName, [director])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoArtist, [director, email, email])
                self.connection.commit()

            self.cursor.execute(selectArtistRole, [director, roles[0]])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoArtistRole, [director, roles[0], email, email])
                self.connection.commit()

        if (item['stars'] is not None):
            for star in item['stars']:
                self.cursor.execute(selectArtistByName, [star])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist, [star, email, email])
                    self.connection.commit()
    
                self.cursor.execute(selectArtistRole, [star, roles[1]])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [star, roles[1], email, email])
                    self.connection.commit()

        return item

class MoviePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        rate = item['rate']
        votes = item['votes']
        link = item['link']
        metascore = item['metascore']
        genre = item['genre']
        
        self.cursor.execute(selectMovieByLink, [link])
        if (self.cursor.rowcount == 0):
            self.cursor.execute(insertIntoMovie, [item['name'], item['year'], rate, votes, link, metascore, item['minutes'], email, email])
        else:
            self.cursor.execute(updateMovie, [rate, votes, metascore, email, link])
        self.connection.commit()
        
        for _genre in item['genres']:
            self.cursor.execute(selectMovieGenre, [_genre, link])
            index = item['index'] if _genre.lower() == genre else None
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoMovieGenre, [index, _genre, link, email, email])
            if (_genre.lower() == genre):
                self.cursor.execute(updateMovieGenre, [index, email, _genre, link]) 
            self.connection.commit()
        
        for director in item['directors']:
            self.cursor.execute(selectMovieArtistRole, [director, roles[0], link])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoMovieArtistRole, [director, roles[0], link, email, email])
                self.connection.commit()
        
        if (item['stars'] is not None):
            for star in item['stars']:
                self.cursor.execute(selectMovieArtistRole, [star, roles[1], link])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoMovieArtistRole, [star, roles[1], link, email, email])
                    self.connection.commit()

        return item
