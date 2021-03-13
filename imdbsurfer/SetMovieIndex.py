import psycopg2

selectSetMovieIndex = 'select set_movie_index();'
psycopg_connect = 'dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''1mdbsurf3r'''

class SetMovieIndex(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()

    def process(self):
        self.cursor.execute(selectSetMovieIndex)
        self.connection.commit()
