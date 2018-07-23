-- FUNCTION: public.invert_value(numeric)

-- DROP FUNCTION public.invert_value(numeric);

CREATE OR REPLACE FUNCTION public.invert_value(
	oldvalue numeric)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$

DECLARE newvalue decimal;
BEGIN
	newvalue = 10 / oldvalue;
	RETURN newvalue;
END;

$BODY$;

ALTER FUNCTION public.invert_value(numeric)
    OWNER TO postgres;
