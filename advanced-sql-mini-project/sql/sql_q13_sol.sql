use euro_cup_2016;

-- Write a SQL query to find all the defenders who scored a goal for their teams

select distinct player_name from player_mast 
join goal_details using(player_id)  
where posi_to_play = 'DF'
order by player_name;