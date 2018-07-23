-- FUNCTION: public.get_movie_index(integer, integer, integer)

-- DROP FUNCTION public.get_movie_index(integer, integer, integer);

CREATE OR REPLACE FUNCTION public.get_movie_index(
	_movie_id integer,
	_genre_id integer,
	_type_id integer)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$

DECLARE _index decimal;
	min_index decimal;
	max_index decimal;
	min_metascore decimal;
	max_metascore decimal;
	min_votes decimal;
	max_votes decimal;
	min_rate decimal;
	max_rate decimal;
BEGIN
	select min(rate) into min_rate from imdbsurfer_movie;
	select max(rate) into max_rate from imdbsurfer_movie;
	select min(metascore) into min_metascore from imdbsurfer_movie;
	select max(metascore) into max_metascore from imdbsurfer_movie;
	select min(votes) into min_votes from imdbsurfer_movie;
	select max(votes) into max_votes from imdbsurfer_movie;
	select min(index) into min_index from imdbsurfer_moviegenre;
	select max(index) into max_index from imdbsurfer_moviegenre;

	select case
		when m.metascore is not null and mg.index is not null
			then round((
				rescale(m.rate, min_rate, max_rate, 1, 10) * 2.5
				+ rescale(m.metascore, min_metascore, max_metascore, 1, 10) * 2.5
				+ rescale(m.votes, min_votes, max_votes, 1, 10) * 2.5
				+ invert_value(rescale(mg.index, min_index, max_index, 1, 10)) * 2.5
				) / 10, 2)
		when m.metascore is null and mg.index is not null
			then round((
				rescale(m.rate, min_rate, max_rate, 1, 10) * 3
				+ rescale(m.votes, min_votes, max_votes, 1, 10) * 3
				+ invert_value(rescale(mg.index, min_index, max_index, 1, 10)) * 3
				) / 10, 2)
		else round((
				rescale(m.rate, min_rate, max_rate, 1, 10) * 4
				+ rescale(m.votes, min_votes, max_votes, 1, 10) * 4
				) / 10, 2)
		end as cindex into _index
	from imdbsurfer_movie m
		inner join imdbsurfer_moviegenre mg on mg.movie_id=m.id and m.id = _movie_id
		inner join imdbsurfer_genre g on g.id=mg.genre_id and g.id = _genre_id
		inner join imdbsurfer_type t on t.id=mg.type_id and t.id = _type_id;
	RETURN _index;
END;

$BODY$;

ALTER FUNCTION public.get_movie_index(integer, integer, integer)
    OWNER TO postgres;
