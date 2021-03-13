use euro_cup_2016;

-- Write a SQL query to find the referees who booked the most number of players.

select r.referee_name, count(distinct p.player_id) as player_count from referee_mast as r
join match_mast as m
on m.referee_id = r.referee_id
join player_booked as p
on p.match_no = m.match_no
group by r.referee_name
order by player_count desc;


