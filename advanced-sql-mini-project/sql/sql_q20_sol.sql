use euro_cup_2016;

-- Write a SQL query to find the substitute players who came into the field in the firsthalf of play, 
-- within a normal play schedule.

select p2.player_name from player_in_out as p1
join player_mast as p2
on p1.player_id = p2.player_id
where p1.play_half = 1 and 
p1.play_schedule = 'NT';