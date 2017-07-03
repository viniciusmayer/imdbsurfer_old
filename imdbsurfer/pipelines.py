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

import psycopg2

selectGenreByName = 'select id from imdbsurfer_genre where name = ''\'{0}''\';'
insertIntoGenre = 'INSERT INTO imdbsurfer_genre(dh_create, dh_update, name, user_create_id, user_update_id) VALUES (now(), now(), ''\'{0}''\', ({1}), ({2}));'
selectUserByEmail = 'select id from auth_user where email = ''\'viniciusmayer@gmail.com''\''


selectArtistByName = 'SELECT id FROM imdbsurfer_artist where name = ''\'{0}''\';'
insertIntoArtist = 'INSERT INTO imdbsurfer_artist(dh_create, dh_update, name, user_create_id, user_update_id) VALUES (now(), now(), ''\'{0}''\', ({1}), ({2}));'

selectRoleByName = 'SELECT id FROM imdbsurfer_role where name = ''\'{0}''\';'
insertIntoRole = 'INSERT INTO imdbsurfer_role(dh_create, dh_update, name, user_create_id, user_update_id) VALUES (now(), now(), ''\'{0}''\', ({1}), ({2}));'

selectArtistRole = 'SELECT id FROM imdbsurfer_artistrole where artist_id = ({0}) and role_id = ({1});'
insertIntoArtistRole = 'INSERT INTO imdbsurfer_artistrole(dh_create, dh_update, artist_id, role_id, user_create_id, user_update_id) VALUES (now(), now(), ({0}), ({1}), ({2}), ({3}));'

class ImdbsurferPipeline(object):
    
    def __init__(self):
        self.connection = psycopg2.connect('dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''viniciusmayer''')
        self.cursor = self.connection.cursor()
          
    def process_item(self, item, spider):
        for genre in item['genres']:
            try:
                self.cursor.execute(selectGenreByName.format(genre))
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoGenre.format(genre, selectUserByEmail, selectUserByEmail))
                    self.connection.commit()
            except Exception as e:
                print(e)
        
        roles = ['Director', 'Star']
        for role in roles:
            try:
                self.cursor.execute(selectRoleByName.format(role))
                if self.cursor.rowcount == 0:
                    self.cursor.execute(insertIntoRole.format(role, selectUserByEmail, selectUserByEmail))
                    self.cursor.commit()
            except Exception as e:
                print(e)                            
                
        for director in item['directors']:
            try:
                self.cursor.execute(selectArtistByName.format(director))
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist.format(director, selectUserByEmail, selectUserByEmail))
                    self.connection.commit()
                self.cursor.execute(selectArtistRole.format(selectArtistByName.format(director), selectRoleByName.format(roles[0])))
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole.format(selectArtistByName.format(director), selectRoleByName.format(roles[0]), selectUserByEmail, selectUserByEmail))
                    self.connection.commit()
            except Exception as e:
                print(e)
        
        for star in item['stars']:
            try:
                self.cursor.execute(selectArtistByName.format(star))
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtist.format(star, selectUserByEmail, selectUserByEmail))
                    self.connection.commit()
                self.cursor.execute(selectArtistRole.format(selectArtistByName.format(star), selectRoleByName.format(roles[1])))
                if (self.cursor.rowcount == 0):
                    self.cursor.execute(insertIntoArtistRole.format(selectArtistByName.format(star), selectRoleByName.format(roles[1]), selectUserByEmail, selectUserByEmail))
                    self.connection.commit()
            except Exception as e:
                print(e)

        return item