use euro_cup_2016;

-- Write a SQL query to find the goalkeeper’s name and jersey number, playing for Germany, 
-- who played in Germany’s group stage matches.

select distinct p.player_name, p.jersey_no 
from player_mast as p
join match_details as m
ON p.player_id = m.player_gk
join soccer_country as c
ON c.country_id = m.team_id
where c.country_name = 'Germany' and
m.play_stage = 'G';