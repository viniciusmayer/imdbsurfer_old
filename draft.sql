select
	m.rate
	, round(rescale(m.rate, (select min(rate) from imdbsurfer_movie), (select max(rate) from imdbsurfer_movie), 1, 10), 2) as crate
	, m.metascore
	, round(rescale(m.metascore, (select min(metascore) from imdbsurfer_movie), (select max(metascore) from imdbsurfer_movie), 1, 10), 2) as cmetascore
	, m.votes
	, round(rescale(m.votes, (select min(votes) from imdbsurfer_movie), (select max(votes) from imdbsurfer_movie), 1, 10), 2) as cvotes
	, mg.index as gindex
	, round(invert_value(rescale(mg.index, (select min(index) from imdbsurfer_moviegenre), (select max(index) from imdbsurfer_moviegenre), 1, 10)), 2) as cindex
	, m.index as mindex
from imdbsurfer_movie m
	inner join imdbsurfer_moviegenre mg on mg.movie_id=m.id
		--and m.metascore is not null
		--and mg.index is not null
	inner join imdbsurfer_genre g on g.id=mg.genre_id
	inner join imdbsurfer_type t on t.id=mg.type_id
order by m.index desc