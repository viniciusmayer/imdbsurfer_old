import psycopg2

updateMovie = 'update imdbsurfer_movie m'\
    ' set index = get_movie_index(m.id, g.id, t.id)'\
    ' from imdbsurfer_moviegenre mg, imdbsurfer_genre g, imdbsurfer_type t'\
    ' where m.id=mg.movie_id and g.id=mg.genre_id and t.id=mg.type_id;'

psycopg_connect = 'dbname=''imdbsurfer'' user=''imdbsurfer'' host=''localhost'' password=''v1n1c1u5'''
class SetMovieIndex(object):
    def __init__(self):
        self.connection = psycopg2.connect(psycopg_connect)
        self.cursor = self.connection.cursor()
        
    def process(self):
        self.cursor.execute(updateMovie)
        self.connection.commit()
