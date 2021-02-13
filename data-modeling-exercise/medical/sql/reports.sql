USE medical;

select p.patient_name from Patient p;

-- Show patients, dates of birth and description of diagnosis
 
SELECT p.patient_name, p.date_of_birth, d.description
from Patient p 
join  Encounter e on e.patient_id = p.patient_id
join  DiagnosisEvent de on de.encounter_id = e.encounter_id
join  Diagnosis d on d.diagnosis_code = de.diagnosis_code;