use euro_cup_2016;

-- Write a SQL query to find referees and the number of bookings they made for the entire tournament. 
-- Sort your answer by the number of bookings in descending order

select r.referee_name, count(p.player_id) as booking_count from referee_mast as r
join match_mast as m
on m.referee_id = r.referee_id
join player_booked as p
on p.match_no = m.match_no
group by r.referee_name
order by booking_count desc;