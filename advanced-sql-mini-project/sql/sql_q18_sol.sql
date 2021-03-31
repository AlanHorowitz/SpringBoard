use euro_cup_2016;

-- Write a SQL query to find the highest number of foul cards given in one match

select max(cards.num_cards) 
from
(select match_no, count(*) as 'num_cards' from player_booked
group by match_no) as cards; 