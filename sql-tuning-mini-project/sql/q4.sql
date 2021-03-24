USE springboardopt;

-- -------------------------------------
SET @v1 = 1612521;
SET @v2 = 1145072;
SET @v3 = 1828467;
SET @v4 = 'MGT382';
SET @v5 = 'Amber Hill';
SET @v6 = 'MGT';
SET @v7 = 'EE';			  
SET @v8 = 'MAT';

-- 4. List the names of students who have taken a course taught by professor v5 (name).

-- Bottleneck: Full scan being run on four tables 
-- Found it by: checking whether index existed EXPLAIN shows type = ALL
-- Resolved by adding indexes to the four tables
-- I couldn't identify an alternative solution to a 4 way join.

CREATE INDEX crsCode_semester_idx on Transcript (crsCode, semester);
CREATE INDEX id_idx on Student (id);
CREATE INDEX name_idx on Professor (name);
CREATE INDEX profId_idx on Teaching (profId); 

SELECT name FROM Student,
	(SELECT studId FROM Transcript,
		(SELECT crsCode, semester FROM Professor
			JOIN Teaching
			WHERE Professor.name = @v5 AND Professor.id = Teaching.profId) as alias1
	WHERE Transcript.crsCode = alias1.crsCode AND Transcript.semester = alias1.semester) as alias2
WHERE Student.id = alias2.studId;

DROP INDEX crsCode_semester_idx on Transcript;
DROP INDEX id_idx on Student;
DROP INDEX name_idx on Professor;
DROP INDEX profId_idx on Teaching; 

