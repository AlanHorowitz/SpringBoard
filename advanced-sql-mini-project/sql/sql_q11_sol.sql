use euro_cup_2016;

-- Write a SQL query to find the players, their jersey number, and playing club 
-- who were the goalkeepers for England in EURO Cup 2016.

select p.player_name, p.jersey_no, p.playing_club from player_mast as p
join soccer_country as c
on p.team_id = c.country_id
where p.posi_to_play = 'GK' and
c.country_name = 'England';
