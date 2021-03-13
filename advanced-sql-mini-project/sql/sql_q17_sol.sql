use euro_cup_2016;

-- Write a SQL query to find the country where the most assistant referees come from
-- ,and the count of the assistant referees.

select c.country_name as Country,
count(*) OVER (PARTITION by r.country_id) as 'Total assistant refs for country',
count(*) OVER () as 'Overall Total Assistant refs'
from asst_referee_mast r
join soccer_country as c
on c.country_id = r.country_id
order by 2 desc limit 1;