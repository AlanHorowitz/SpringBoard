use euro_cup_2016;

-- Write a SQL query to find the number of matches that were won by penalty shootout.

select count(*) from match_mast
where decided_by = 'P';