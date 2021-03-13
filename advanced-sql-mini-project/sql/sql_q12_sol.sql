use euro_cup_2016;

-- Write a SQL query that returns the total number of goals scored by each position on each country’s team. 
-- Do not include positions which scored no goals.

select 
c.country_name as Country, 
p.posi_to_play as Position,
count(*) as 'Goal Count' 
from goal_details as g
join soccer_country as c
on g.team_id = c.country_id
join player_mast as p
on g.player_id = p.player_id
group by c.country_name, p.posi_to_play
order by c.country_name, p.posi_to_play;