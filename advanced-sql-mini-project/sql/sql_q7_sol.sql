use euro_cup_2016;

-- Write a SQL query to find all the venues where matches with penalty shootouts were played

select v.venue_name 
from soccer_venue as v
join match_mast as m
on m.venue_id = v.venue_id
where m.decided_by = 'P';