use euro_cup_2016;

-- Write a SQL query to compute a list showing the number of substitutions that happened 
-- in various stages of play for the entire tournament.

select CASE 
	WHEN m.play_stage = 'G' THEN 'Group Stage' 
    WHEN m.play_stage = 'R' THEN 'Round of 16'
    WHEN m.play_stage = 'Q' THEN 'Quarter Final' 
    WHEN m.play_stage = 'S' THEN 'Semi Final' 
    WHEN m.play_stage = 'F' THEN 'Final' 
    END as stage, 
count(p.player_id) as substitions from player_in_out as p
join match_mast as m on m.match_no = p.match_no
group by m.play_stage;

