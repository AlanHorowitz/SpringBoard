use soccer;

delete from Match_Results;
delete from Goals;
delete from Players;
delete from Matches;
delete from Teams;

insert into Teams
(team_name)
values ('team1'), ('team2'), ('team3');

insert into Players (player_id, player_name, team_name)
values 
(1, 'player_1_team_1', 'team1'),
(2, 'player_2_team_1', 'team1'),
(3, 'player_1_team_2', 'team2'),
(4, 'player_2_team_2', 'team2');

insert into Matches (match_id, home_team, visiting_team)
values
(1, 'team1', 'team2'),
(2, 'team2', 'team1'),
(3, 'team1', 'team2'),
(4, 'team2', 'team1');

insert into Goals (match_id, player_id, number_of_goals)
values
(1,1,1),
(1,2,1),
(1,3,1),
(1,4,2),
(2,2,1),
(2,3,2),
(3,1,2),
(4,1,1),
(4,3,1);

-- show total goals for each player that scored

select p.player_name, sum(g.number_of_goals) from Players p
join Goals g on p.player_id = g.player_id
group by p.player_name;

-- Show total goals for each team

select p.team_name, sum(g.number_of_goals) from Players p
join Goals g on p.player_id = g.player_id
group by p.team_name;

insert into Match_Results (match_id, team_name, goals_for, goals_against)
select 
	m.match_id, 
    m.home_team as 'team_name',
	(select coalesce(sum(g.number_of_goals),0) from Goals g
		join Players p on p.player_id = g.player_id
		where p.team_name = m.home_team AND g.match_id = m.match_id),    
	(select coalesce(sum(g.number_of_goals),0) from Goals g
		join Players p on p.player_id = g.player_id
		where p.team_name = m.visiting_team AND g.match_id = m.match_id)
from Matches m;

insert into Match_Results (match_id, team_name, goals_for, goals_against)
select 
	m.match_id, 
    m.visiting_team as 'team_name',
	(select coalesce(sum(g.number_of_goals),0) from Goals g
		join Players p on p.player_id = g.player_id
		where p.team_name = m.visiting_team AND g.match_id = m.match_id),    
	(select coalesce(sum(g.number_of_goals),0) from Goals g
		join Players p on p.player_id = g.player_id
		where p.team_name = m.home_team AND g.match_id = m.match_id)
from Matches m;

update Match_Results 
set 
win = 
	CASE
		WHEN goals_for > goals_against THEN 1
		ELSE 0
	END,
lose = 
	CASE
		WHEN goals_against > goals_for THEN 1		
		ELSE 0
	END,
tie = 
	CASE
		WHEN goals_for = goals_against THEN 1
		ELSE 0
	END,
points = 
	CASE
		WHEN goals_for > goals_against THEN 3
		WHEN goals_for = goals_against THEN 1
		ELSE 0
	END;    
    
select * from Match_Results;

-- Show standings

select team_name as 'team',
 sum(win) as 'wins', 
 sum(lose) as 'losses', 
 sum(tie) as 'ties', 
 sum(points) as 'points'
 from Match_Results
group by team_name
order by points desc
