USE craigslist;

delete from Posts;
delete from Users;
delete from Regions;

insert into Regions (region_name) values ('France'),('Germany'),('USA');

insert into Users (user_id, preferred_region) values
(1, 'France'), (2,NULL), (3,'Germany');

insert into Posts
values
(1,1,'Title1',NULL,'362 owen ave','Germany','Hobbies'),
(2,1,'Title1',NULL,'362 owen ave','France','Hobbies'),
(3,1,'Title1','special order','362 owen ave','USA','Hobbies');

select u.user_id, u.preferred_region, p.region
from Users u
join Posts p on p.user_id = u.user_id;