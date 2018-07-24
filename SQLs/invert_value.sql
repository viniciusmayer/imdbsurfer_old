-- FUNCTION: public.invert_value(numeric)

-- DROP FUNCTION public.invert_value(numeric);

CREATE OR REPLACE FUNCTION public.invert_value(
	oldvalue numeric)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

BEGIN
	RETURN (10 / oldvalue);
END;

$BODY$;

ALTER FUNCTION public.invert_value(numeric)
    OWNER TO postgres;
