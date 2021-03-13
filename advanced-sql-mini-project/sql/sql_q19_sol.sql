use euro_cup_2016;

-- Write a SQL query to find the number of captains who were also goalkeepers.

select count(distinct c.player_captain) as 'GK captains' 
from match_captain as c
join player_mast as p
on p.player_id = c.player_captain
where p.posi_to_play = 'GK';

