USE medical;

LOAD DATA
INFILE 'facility.csv'
INTO TABLE Facility
FIELDS terminated by ','
enclosed by '"';

LOAD DATA
INFILE 'provider.csv'
INTO TABLE Provider
FIELDS terminated by ','
enclosed by '"';

LOAD DATA
INFILE 'patient.csv'
INTO TABLE Patient
FIELDS terminated by ','
enclosed by '"';

LOAD DATA
INFILE 'encounter.csv'
INTO TABLE Encounter
FIELDS terminated by ','
enclosed by '"'
(facility_id,
 provider_id,
 patient_id,
 room_id,
 encounter_begin_time,
 encounter_end_time);
 
LOAD DATA
INFILE 'diagnosis.csv'
INTO TABLE Diagnosis
FIELDS terminated by ','
enclosed by '"';

LOAD DATA
INFILE 'diagnosisevent.csv'
INTO TABLE DiagnosisEvent
FIELDS terminated by ','
enclosed by '"';
