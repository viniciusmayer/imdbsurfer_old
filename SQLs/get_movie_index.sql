-- FUNCTION: public.get_movie_index(integer, integer, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric)

-- DROP FUNCTION public.get_movie_index(integer, integer, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric);

CREATE OR REPLACE FUNCTION public.get_movie_index(
	_movie_id integer,
	_genre_id integer,
	_type_id integer,
	min_index numeric,
	max_index numeric,
	min_metascore numeric,
	max_metascore numeric,
	min_votes numeric,
	max_votes numeric,
	min_rate numeric,
	max_rate numeric,
	min_year numeric,
	max_year numeric,
	index_weight numeric,
	metascore_weight numeric,
	votes_weight numeric,
	rate_weight numeric,
	year_weight numeric)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE _index decimal;
BEGIN
	select case
		when m.metascore is not null and mg.index is not null --completo
			then (m.rate * rate_weight
				  + (m.metascore / 10) * metascore_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + (10 / rescale(mg.index, min_index, max_index, 1, 10)) * index_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				) / 10
		when m.metascore is not null and mg.index is null --não tem index
			then (m.rate * rate_weight
				  + (m.metascore / 10) * metascore_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				) / 10
		when m.metascore is null and mg.index is not null -- não tem metascore
			then (m.rate * rate_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + (10 / rescale(mg.index, min_index, max_index, 1, 10)) * index_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				) / 10
		else (m.rate * rate_weight --não tem index e não tem metascore
			  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
			  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
			) / 10
		end as cindex into _index
	from imdbsurfer_movie m
		inner join imdbsurfer_moviegenre mg on mg.movie_id=m.id and m.id = _movie_id
		inner join imdbsurfer_genre g on g.id=mg.genre_id and g.id = _genre_id
		inner join imdbsurfer_type t on t.id=mg.type_id and t.id = _type_id;
	RETURN round(_index, 2);
END;

$BODY$;

ALTER FUNCTION public.get_movie_index(integer, integer, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric)
    OWNER TO imdbsurfer;
