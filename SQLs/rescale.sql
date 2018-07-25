-- FUNCTION: public.rescale(numeric, numeric, numeric, numeric, numeric)

-- DROP FUNCTION public.rescale(numeric, numeric, numeric, numeric, numeric);

CREATE OR REPLACE FUNCTION public.rescale(
	oldvalue numeric,
	oldmin numeric,
	oldmax numeric,
	newmin numeric,
	newmax numeric)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE oldrange decimal;
	newrange decimal;
	newvalue decimal;
BEGIN
	oldrange = (oldmax - oldmin);
	newrange = (newmax - newmin);
	RETURN (((oldvalue - oldmin) * newrange) / oldrange) + newmin;
END;

$BODY$;

ALTER FUNCTION public.rescale(numeric, numeric, numeric, numeric, numeric)
    OWNER TO postgres;
