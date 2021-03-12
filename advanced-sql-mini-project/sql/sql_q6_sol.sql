use euro_cup_2016;

-- Write a SQL query to find the number of matches that were won by a single point, 
-- but do not include matches decided by penalty shootout.

-- Note: self-join yields 4 rows per match_no.  First 2 WHERE clauses reduce these to one
-- of interest (Draws are irrelevant).

select count(md1.match_no)
from match_details as md1  
join match_details as md2 
on md1.match_no = md2.match_no
WHERE 
md1.team_id != md2.team_id and
md1.win_lose = 'W' and
md1.goal_score - md2.goal_score = 1 and
md1.decided_by = 'N';

