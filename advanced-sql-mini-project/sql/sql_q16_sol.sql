use euro_cup_2016;

-- Write a SQL query to find referees and the number of matches they worked in each venue.

select r.referee_name, v.venue_name, count(m.match_no) as 'Match Count'
from referee_mast as r
join match_mast as m
on m.referee_id = r.referee_id
join soccer_venue as v
on v.venue_id = m.venue_id
group by r.referee_name, v.venue_name;