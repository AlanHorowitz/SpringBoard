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
     
-- 5. List the names of students who have taken a course from department v6 (deptId), but not v7.
SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;

-- Bottleneck: Transcript table is read twice.  Also, the dependent subqueries seem suboptimal somehow.
-- Found it by: inspection
-- Resolved by identifying needed student ids via aggregating two derived columns plus HAVING
-- create index deptId_idx ON Course (deptId) in addition to previous indices
-- 6X performance improvement.

CREATE INDEX id_idx on Student (id);
CREATE INDEX crsCode_idx on Transcript (crsCode);
CREATE INDEX deptID_idx on Course (deptID);

EXPLAIN SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'PRIMARY', 'Course', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '26', '100.00', 'Using where'
'1', 'PRIMARY', 'Transcript', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'springboardopt.Course.crsCode', '1', '100.00', 'Using where'
'1', 'PRIMARY', 'Student', NULL, 'ref', 'id_idx', 'id_idx', '5', 'springboardopt.Transcript.studId', '1', '100.00', 'Using where'
'3', 'DEPENDENT SUBQUERY', 'Course', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '32', '100.00', 'Using where'
'3', 'DEPENDENT SUBQUERY', 'Transcript', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'springboardopt.Course.crsCode', '1', '100.00', 'Using where'
*/
SET profiling=1;
SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;
set profiling=0;
/*
# Query_ID, Duration, Query
'385', '0.00807325', 'SELECT * FROM Student, \n	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode\n	AND studId NOT IN\n	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias\nWHERE Student.id = alias.studId\nLIMIT 0, 50'
*/

--- Solution to problem 5

EXPLAIN SELECT s.name 
FROM Student s
JOIN (SELECT 
	     studId, 
		 SUM(CASE WHEN c.deptId = @v6 
				  THEN 1 
                  ELSE 0
			 END) as v6_cnt,
		 SUM(CASE WHEN c.deptId = @v7 
				  THEN 1 
				  ELSE 0
			 END) as v7_cnt
	 FROM Transcript t 
     JOIN Course c
	 ON c.crsCode = t.crsCode
     GROUP by studId
     HAVING v6_cnt > 0 AND v7_cnt = 0) a
ON s.id = a.studId;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'PRIMARY', '<derived2>', NULL, 'ALL', NULL, NULL, NULL, NULL, '103', '100.00', 'Using where'
'1', 'PRIMARY', 's', NULL, 'ref', 'id_idx', 'id_idx', '5', 'a.studId', '1', '100.00', NULL
'2', 'DERIVED', 'c', NULL, 'ALL', NULL, NULL, NULL, NULL, '100', '100.00', 'Using where; Using temporary'
'2', 'DERIVED', 't', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'springboardopt.c.crsCode', '1', '100.00', NULL
*/

set profiling=1;
SELECT s.name 
FROM Student s
JOIN (SELECT 
	     studId, 
		 SUM(CASE WHEN c.deptId = @v6 
				  THEN 1 
                  ELSE 0
			 END) as v6_cnt,
		 SUM(CASE WHEN c.deptId = @v7 
				  THEN 1 
				  ELSE 0
			 END) as v7_cnt
	 FROM Transcript t 
     JOIN Course c
	 ON c.crsCode = t.crsCode
     GROUP by studId
     HAVING v6_cnt > 0 AND v7_cnt = 0) a
ON s.id = a.studId;
SET profiling=0;
/*
# Query_ID, Duration, Query
'387', '0.00130400', 'SELECT s.name \nFROM Student s\nJOIN (SELECT \n	     studId, \n		 SUM(CASE WHEN c.deptId = @v6 \n				  THEN 1 \n                  ELSE 0\n			 END) as v6_cnt,\n		 SUM(CASE WHEN c.deptId = @v7 \n				  THEN 1 \n				  ELSE 0\n			 END) as v7_cnt\n	 FROM Transcript t \n     JOIN Course c\n	 ON c.crsCode = t.crsCode\n   '
*/

DROP INDEX id_idx on Student;
DROP INDEX crsCode_idx on Transcript;
DROP INDEX deptID_idx on Course;

