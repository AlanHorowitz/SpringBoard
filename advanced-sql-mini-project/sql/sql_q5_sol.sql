use euro_cup_2016;

-- Write a SQL query to find the number of bookings that happened in stoppage time.

select count(*) from player_booked
where play_schedule = 'ST';