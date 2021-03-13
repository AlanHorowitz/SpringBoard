use euro_cup_2016;

-- Write a SQL query to find the match number, date, and score 
-- for matches in which no stoppage time was added in the 1st half

-- I note that the goal_score column match_mast.csv contains strange 
-- month data when both teams score more at least one goal (e.g. 01-Jan. which is a draw)

select match_no, play_date, goal_score
from match_mast
where stop1_sec = 0;