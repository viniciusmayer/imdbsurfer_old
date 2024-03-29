-- FUNCTION: public.set_movie_index()

-- DROP FUNCTION public.set_movie_index();

CREATE OR REPLACE FUNCTION public.set_movie_index(
	)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE min_index decimal;
	max_index decimal;
	min_metascore decimal;
	max_metascore decimal;
	min_votes decimal;
	max_votes decimal;
	min_rate decimal;
	max_rate decimal;
	min_year decimal;
	max_year decimal;
	index_weight decimal := 0.5;
	metascore_weight decimal := 2;
	votes_weight decimal := 3;
	rate_weight decimal := 3;
	year_weight decimal := 1.5;
BEGIN
	select min(rate) into min_rate from imdbsurfer_movie;
	select max(rate) into max_rate from imdbsurfer_movie;
	select min(metascore) into min_metascore from imdbsurfer_movie;
	select max(metascore) into max_metascore from imdbsurfer_movie;
	select min(votes) into min_votes from imdbsurfer_movie;
	select max(votes) into max_votes from imdbsurfer_movie;
	select min(year) into min_year from imdbsurfer_movie;
	select max(year) into max_year from imdbsurfer_movie;
	select min(index) into min_index from imdbsurfer_moviegenre;
	select max(index) into max_index from imdbsurfer_moviegenre;

	update imdbsurfer_movie m
	set last_index = index;

	update imdbsurfer_movie m
    set index = get_movie_index(m.id, g.id, t.id
			, min_index, max_index
			, min_metascore, max_metascore
			, min_votes, max_votes
			, min_rate, max_rate
			, min_year, max_year
			, index_weight, metascore_weight, votes_weight, rate_weight, year_weight)
    from imdbsurfer_moviegenre mg, imdbsurfer_genre g, imdbsurfer_type t
    where m.id=mg.movie_id and g.id=mg.genre_id and t.id=mg.type_id;

    update imdbsurfer_movie m
    set last_update = (index - last_index) / 10;

	RETURN 0;
END;

$BODY$;

ALTER FUNCTION public.set_movie_index()
    OWNER TO imdbsurfer;
