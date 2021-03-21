import psycopg2
import configparser

selectSetMovieIndex = 'select set_movie_index();'


class SetMovieIndex(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('properties.ini')
        host = config['DATABASE']['host']
        schema = config['DATABASE']['schema']
        user = config['DATABASE']['user']
        passw = config['DATABASE']['pass']

        self.connection = psycopg2.connect('dbname={0} user={1} host={2} password={3}'.format(schema, user, host, passw))
        self.cursor = self.connection.cursor()

    def process(self):
        self.cursor.execute(selectSetMovieIndex)
        self.connection.commit()
