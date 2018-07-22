CREATE OR REPLACE FUNCTION set_movie_index() RETURNS integer AS $$
BEGIN
	update imdbsurfer_movie m
	set index = get_movie_index(m.id, g.id, t.id)
	from imdbsurfer_moviegenre mg, imdbsurfer_genre g, imdbsurfer_type t
	where m.id=mg.movie_id and g.id=mg.genre_id and t.id=mg.type_id;
	RETURN 0;
END;
$$ LANGUAGE plpgsql;
