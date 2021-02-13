CREATE DATABASE IF NOT EXISTS medical DEFAULT CHARSET = utf8mb4;
USE medical;

DROP TABLE IF EXISTS Encounter;
DROP TABLE IF EXISTS Facility;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Provider;

CREATE TABLE Facility (
  facility_id int NOT NULL PRIMARY KEY,
  facility_name varchar(255) DEFAULT NULL,
  facility_address varchar(255) DEFAULT NULL,
  number_of_beds int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Provider (
  provider_id int NOT NULL PRIMARY KEY,
  provider_name varchar(255) DEFAULT NULL,
  license_id varchar(255) DEFAULT NULL,
  specialty varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Patient (
  patient_id int NOT NULL PRIMARY KEY,
  patient_name varchar(255) DEFAULT NULL,
  patient_address varchar(255) DEFAULT NULL,
  social_security_number varchar(255) DEFAULT NULL,
  telephone_number varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Encounter (
  encounter_id int auto_increment NOT NULL PRIMARY KEY,
  facility_id int ,
  provider_id int ,
  patient_id int ,
  room_id varchar(4),
  encounter_begin_time datetime,
  encounter_end_time datetime,
  CONSTRAINT fk_facility_id
    FOREIGN KEY (facility_id) 
	REFERENCES Facility(facility_id),
  CONSTRAINT fk_patient_id
    FOREIGN KEY (patient_id) 
	REFERENCES Patient(patient_id),
  CONSTRAINT fk_provider_id
	FOREIGN KEY (provider_id)
    REFERENCES Provider(provider_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




