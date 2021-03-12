use euro_cup_2016;

-- Write a SQL query to find the match number for the game with the 
-- highest number of penalty shots, and which countries played that match.

select m1.match_no, s.country_name from soccer_country s
join match_details as m1
on s.country_id = m1.team_id
where m1.match_no =
	(select m2.match_no from match_details as m2 
	group by m2.match_no
	order by sum(m2.penalty_score) desc
	LIMIT 1);
