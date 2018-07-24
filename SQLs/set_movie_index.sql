-- FUNCTION: public.set_movie_index()

-- DROP FUNCTION public.set_movie_index();

CREATE OR REPLACE FUNCTION public.set_movie_index(
	)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

BEGIN
	update imdbsurfer_movie m
	set index = get_movie_index(m.id, g.id, t.id)
	from imdbsurfer_moviegenre mg, imdbsurfer_genre g, imdbsurfer_type t
	where m.id=mg.movie_id and g.id=mg.genre_id and t.id=mg.type_id;
	RETURN 0;
END;

$BODY$;

ALTER FUNCTION public.set_movie_index()
    OWNER TO postgres;
