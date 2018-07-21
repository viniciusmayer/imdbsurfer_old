# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2


selectIndex = 'select case when m.metascore is not null and mg.index is not null'\
'        then round(round((round(m.rate, 2) * 2.5'\
'            + round(round(m.metascore, 2) / 10, 2) * 2.5'\
'            + round(100/round(mg.index * 10, 2), 2) * 2.5'\
'            + round(round((m.votes - (select min(votes) from imdbsurfer_movie)) * (10 - 0), 2)'\
'                / round(((select max(votes) from imdbsurfer_movie) - (select min(votes) from imdbsurfer_movie)) + 0, 2), 2) * 2.5'\
'            ), 2) / 10, 2)'\
'    when m.metascore is null and mg.index is not null'\
'        then round(round((round(m.rate, 2) * 3'\
'            + round(100/round(mg.index * 10, 1), 2) * 3'\
'            + round(round((m.votes - (select min(votes) from imdbsurfer_movie)) * (10 - 0), 2)'\
'                / round(((select max(votes) from imdbsurfer_movie) - (select min(votes) from imdbsurfer_movie)) + 0, 2), 2) * 3'\
'            ), 2) / 10, 2)'\
'    else round(round((round(m.rate, 2) * 4'\
'        + round(round((m.votes - (select min(votes) from imdbsurfer_movie)) * (10 - 0), 2)'\
'            / round(((select max(votes) from imdbsurfer_movie) - (select min(votes) from imdbsurfer_movie)) + 0, 2), 2) * 4'\
'        ), 2) / 10, 2)'\
'    end as cindex'\
' from imdbsurfer_movie m'\
'    inner join imdbsurfer_moviegenre mg on mg.movie_id=m.id and m.link = %s'\
'    inner join imdbsurfer_genre g on g.id=mg.genre_id and g.name = %s'\
'    inner join imdbsurfer_type t on t.id=mg.type_id and t.name = %s'\
' order by cindex desc'
updateIndex = 'update imdbsurfer_movie m set index = %s'\
' from imdbsurfer_moviegenre mg, imdbsurfer_genre g, imdbsurfer_type t'\
' where m.id=mg.movie_id and m.link = %s'\
'    and g.id=mg.genre_id and g.name = %s'\
'    and t.id=mg.type_id and t.name = %s'

selectUserByEmail = 'select id from auth_user where email = %s'
email = 'viniciusmayer@gmail.com'

selectGenreByName = 'select id from imdbsurfer_genre where name = %s'
insertIntoGenre = 'INSERT INTO imdbsurfer_genre(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectRoleByName = 'SELECT id FROM imdbsurfer_role where name = %s'
insertIntoRole = 'INSERT INTO imdbsurfer_role(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectTypeByName = 'select id from imdbsurfer_type where name = %s'
insertIntoType = 'INSERT INTO imdbsurfer_type(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectArtistByName = 'SELECT id FROM imdbsurfer_artist where name = %s'
insertIntoArtist = 'INSERT INTO imdbsurfer_artist(dh_create, dh_update, name, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)

selectArtistRole = 'SELECT id FROM imdbsurfer_artistrole'\
    ' where artist_id = ({0})'\
        ' and role_id = ({1})'.format(selectArtistByName, selectRoleByName)
insertIntoArtistRole = 'INSERT INTO imdbsurfer_artistrole(dh_create, dh_update, artist_id, role_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectArtistByName, selectRoleByName, selectUserByEmail, selectUserByEmail)

selectMovieByLink = 'SELECT id FROM imdbsurfer_movie where link = %s' 
insertIntoMovie = 'INSERT INTO imdbsurfer_movie(name, year, rate, votes, link, metascore, minutes, watch, watched, dh_create, dh_update, user_create_id, user_update_id)'\
    ' VALUES (%s, %s, %s, %s, %s, %s, %s, False, False, now(), now(), ({0}), ({1}))'.format(selectUserByEmail, selectUserByEmail)
updateMovie = 'UPDATE imdbsurfer_movie SET dh_update=now(), rate=%s, votes=%s, metascore=%s, user_update_id=({0})'\
    ' WHERE link=%s'.format(selectUserByEmail)

selectMovieGenre = 'SELECT id FROM imdbsurfer_moviegenre'\
    ' where genre_id = ({0})'\
        ' and movie_id = ({1})'\
        ' and type_id = ({2})'.format(selectGenreByName, selectMovieByLink, selectTypeByName)
insertIntoMovieGenre = 'INSERT INTO imdbsurfer_moviegenre(dh_create, dh_update, index, genre_id, movie_id, type_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), %s, ({0}), ({1}), ({2}), ({3}), ({4}))'.format(selectGenreByName, selectMovieByLink, selectTypeByName, selectUserByEmail, selectUserByEmail)
updateMovieGenre = 'UPDATE imdbsurfer_moviegenre SET dh_update=now(), index=%s, user_update_id=({0})'\
    ' WHERE genre_id=({1})'\
        ' and movie_id=({2})'\
        ' and type_id = ({2})'.format(selectUserByEmail, selectGenreByName, selectMovieByLink, selectTypeByName)

selectMovieArtistRole = 'SELECT id FROM imdbsurfer_movieartistrole'\
    ' where "artistRole_id" = ({0})'\
        ' and movie_id = ({1})'.format(selectArtistRole, selectMovieByLink)
insertIntoMovieArtistRole = 'INSERT INTO imdbsurfer_movieartistrole(dh_create, dh_update, "artistRole_id", movie_id, user_create_id, user_update_id)'\
    ' VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}))'.format(selectArtistRole, selectMovieByLink, selectUserByEmail, selectUserByEmail)

DIRECTOR = 'Director'
STAR = 'Star'

psycopg_connect = 'dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''v1n1c1u5'''

class TypePipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        _type = item['type']
        self.cursor.execute(selectTypeByName, [_type])
        if (self.cursor.rowcount == 0):
            self.cursor.execute(insertIntoType, [_type, email, email])
            self.connection.commit()
        
        return item

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
        for role in [DIRECTOR, STAR]:
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

            self.cursor.execute(selectArtistRole, [director, DIRECTOR])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoArtistRole, [director, DIRECTOR, email, email])
                self.connection.commit()

        if (item['stars'] is not None):
            for star in item['stars']:
                self.cursor.execute(selectArtistByName, [star])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist, [star, email, email])
                    self.connection.commit()
    
                self.cursor.execute(selectArtistRole, [star, STAR])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole, [star, STAR, email, email])
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
        urlGenre = item['genre']
        _type = item['type']
        
        self.cursor.execute(selectMovieByLink, [link])
        if (self.cursor.rowcount == 0):
            self.cursor.execute(insertIntoMovie, [item['name'], item['year'], rate, votes, link, metascore, item['minutes'], email, email])
        else:
            self.cursor.execute(updateMovie, [rate, votes, metascore, email, link])
        self.connection.commit()
        
        for _genre in item['genres']:
            self.cursor.execute(selectMovieGenre, [_genre, link, _type])
            index = item['index'] if _genre == urlGenre else None
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoMovieGenre, [index, _genre, link, _type, email, email])
            else:
                self.cursor.execute(updateMovieGenre, [index, email, _genre, link, _type])
            self.connection.commit()

        for director in item['directors']:
            self.cursor.execute(selectMovieArtistRole, [director, DIRECTOR, link])
            if (self.cursor.rowcount == 0):
                self.cursor.execute(insertIntoMovieArtistRole, [director, DIRECTOR, link, email, email])
                self.connection.commit()
        
        if (item['stars'] is not None):
            for star in item['stars']:
                self.cursor.execute(selectMovieArtistRole, [star, STAR, link])
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoMovieArtistRole, [star, STAR, link, email, email])
                    self.connection.commit()

        return item
