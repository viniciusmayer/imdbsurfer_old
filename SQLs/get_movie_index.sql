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
	min_year decimal;
	max_year decimal;
	index_weight decimal := 2.25;
	metascore_weight decimal := 2.25;
	votes_weight decimal := 2.25;
	rate_weight decimal := 2.25;
	year_weight decimal := 1;
	weight_adjustment decimal := 0.5;
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

	select case
		when m.metascore is not null and mg.index is not null
			then (m.rate * rate_weight
				  + (m.metascore / 10) * metascore_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + (10 / rescale(mg.index, min_index, max_index, 1, 10)) * index_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				 ) / (rate_weight + metascore_weight + votes_weight + index_weight + year_weight)
		when m.metascore is not null and mg.index is null
			then (m.rate * rate_weight
				  + (m.metascore / 10) * metascore_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				 ) / (rate_weight + metascore_weight + votes_weight + year_weight + weight_adjustment)
		when m.metascore is null and mg.index is not null
			then (m.rate * rate_weight
				  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
				  + (10 / rescale(mg.index, min_index, max_index, 1, 10)) * index_weight
				  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
				 ) / (rate_weight + votes_weight + index_weight + year_weight + weight_adjustment)
		else (m.rate * rate_weight
			  + rescale(m.votes, min_votes, max_votes, 0, 10) * votes_weight
			  + rescale(m.year, min_year, max_year, 1, 10) * year_weight
			 ) / (rate_weight + votes_weight + year_weight + (weight_adjustment * 2))
		end as cindex into _index
	from imdbsurfer_movie m
		inner join imdbsurfer_moviegenre mg on mg.movie_id=m.id and m.id = _movie_id
		inner join imdbsurfer_genre g on g.id=mg.genre_id and g.id = _genre_id
		inner join imdbsurfer_type t on t.id=mg.type_id and t.id = _type_id;
	RETURN round(_index, 2);
END;

$BODY$;

ALTER FUNCTION public.get_movie_index(integer, integer, integer)
    OWNER TO postgres;
