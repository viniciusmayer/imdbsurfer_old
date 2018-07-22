CREATE OR REPLACE FUNCTION rescale(oldvalue decimal
	, oldmin decimal
	, oldmax decimal
	, newmin decimal
	, newmax decimal) RETURNS decimal AS $$
DECLARE oldrange decimal;
	newrange decimal;
	newvalue decimal;
BEGIN
	oldrange = (oldmax - oldmin);
	newrange = (newmax - newmin);
	newvalue = (((oldvalue - oldmin) * newrange) / oldrange) + newmin;
	RETURN newvalue;
END;
$$ LANGUAGE plpgsql;
