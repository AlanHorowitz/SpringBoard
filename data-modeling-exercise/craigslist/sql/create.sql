CREATE DATABASE IF NOT EXISTS craigslist DEFAULT CHARSET = utf8mb4;
USE craigslist;

DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Regions;

CREATE TABLE Regions (
  region_name varchar(50) NOT NULL PRIMARY KEY  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Users (
  user_id int NOT NULL PRIMARY KEY,
  preferred_region varchar(50) DEFAULT NULL,
  CONSTRAINT fk_preferred_region
    FOREIGN KEY (preferred_region) 
	REFERENCES Regions(region_name)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Posts (
  post_id int NOT NULL PRIMARY KEY,
  user_id int NOT NULL,
  title varchar(50) DEFAULT NULL,
  text varchar(255) DEFAULT NULL,
  location varchar(255),
  region varchar(50) NOT NULL,
  category varchar(50),
  CONSTRAINT fk_user_id
    FOREIGN KEY (user_id) 
	REFERENCES Users(user_id), 
  CONSTRAINT fk_region
    FOREIGN KEY (region) 
	REFERENCES Regions(region_name)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

