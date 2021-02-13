CREATE DATABASE IF NOT EXISTS medical DEFAULT CHARSET = utf8mb4;
USE medical;

DROP TABLE IF EXISTS DiagnosisEvent;
DROP TABLE IF EXISTS Diagnosis;
DROP TABLE IF EXISTS Encounter;
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
  date_of_birth date,
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

CREATE TABLE Diagnosis (
  diagnosis_code varchar(20) NOT NULL PRIMARY KEY,
  description varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DiagnosisEvent (
  encounter_id int NOT NULL,
  diagnosis_code varchar(20) NOT NULL,
  notes varchar(255),
  PRIMARY KEY (encounter_id, diagnosis_code),
  CONSTRAINT fk_encounter_id
    FOREIGN KEY (encounter_id) 
	REFERENCES Encounter(encounter_id),
  CONSTRAINT fk_diagnosis_code
    FOREIGN KEY (diagnosis_code) 
	REFERENCES Diagnosis(diagnosis_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

