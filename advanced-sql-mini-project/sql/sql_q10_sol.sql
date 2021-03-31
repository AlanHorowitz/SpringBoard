use euro_cup_2016;

-- Write a SQL query to find all available information about the players under contract
-- to Liverpool F.C. playing for England in EURO Cup 2016

select p.* from player_mast as p
join soccer_country as c
on p.team_id = c.country_id
where p.playing_club = 'Liverpool' and
c.country_name = 'England';