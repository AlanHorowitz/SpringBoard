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

-- 6. List the names of students who have taken all courses offered by department v8 (deptId).
SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;

-- Bottleneck: "crsCode IN (SELECT crsCode FROM Teaching)" serves no purpose and can be removed.
-- Found it by: inspection
-- Resolved by removing the needless clauses.  Also changed IN subquery to simple join
-- Added three indices.
-- 4x performance improvement

CREATE INDEX id_idx on Student (id);
CREATE INDEX crsCode_idx on Transcript (crsCode);
CREATE INDEX deptID_idx on Course (deptID);

EXPLAIN SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'PRIMARY', '<derived2>', NULL, 'ALL', NULL, NULL, NULL, NULL, '2', '100.00', 'Using where'
'1', 'PRIMARY', 'Student', NULL, 'ref', 'id_idx', 'id_idx', '5', 'alias.studId', '1', '100.00', NULL
'2', 'DERIVED', '<subquery3>', NULL, 'ALL', NULL, NULL, NULL, NULL, NULL, '100.00', 'Using where; Using temporary'
'2', 'DERIVED', 'Transcript', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', '<subquery3>.crsCode', '1', '100.00', NULL
'3', 'MATERIALIZED', 'Course', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '19', '100.00', NULL
'3', 'MATERIALIZED', 'Teaching', NULL, 'ALL', NULL, NULL, NULL, NULL, '100', '10.00', 'Using where; Using join buffer (hash join)'
'5', 'UNCACHEABLE SUBQUERY', 'Course', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '19', '100.00', 'Using where'
'5', 'UNCACHEABLE SUBQUERY', '<subquery6>', NULL, 'eq_ref', '<auto_distinct_key>', '<auto_distinct_key>', '1023', 'springboardopt.Course.crsCode', '1', '100.00', NULL
'6', 'MATERIALIZED', 'Teaching', NULL, 'ALL', NULL, NULL, NULL, NULL, '100', '100.00', NULL
*/

SET profiling=1;
SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;
set profiling=0;
/*
# Query_ID, Duration, Query
'397', '0.00365075', 'SELECT name FROM Student,\n	(SELECT studId\n	FROM Transcript\n		WHERE crsCode IN\n		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))\n		GROUP BY studId\n		HAVING COUNT(*) = \n			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM '
*/

-- Solution to problem 6

EXPLAIN SELECT s.name FROM Student s,
	(SELECT t.studId
	FROM Transcript t
		JOIN Course c 
        ON c.crsCode = t.crsCode AND c.deptId = @v8
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8)) as alias
WHERE s.id = alias.studId;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'PRIMARY', '<derived2>', NULL, 'ALL', NULL, NULL, NULL, NULL, '19', '100.00', 'Using where'
'1', 'PRIMARY', 's', NULL, 'ref', 'id_idx', 'id_idx', '5', 'alias.studId', '1', '100.00', NULL
'2', 'DERIVED', 'c', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '19', '100.00', 'Using where; Using temporary'
'2', 'DERIVED', 't', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'springboardopt.c.crsCode', '1', '100.00', NULL
'3', 'UNCACHEABLE SUBQUERY', 'Course', NULL, 'ref', 'deptID_idx', 'deptID_idx', '1023', 'const', '19', '100.00', 'Using index'
*/

set profiling=1;
SELECT s.name FROM Student s,
	(SELECT t.studId
	FROM Transcript t
		JOIN Course c 
        ON c.crsCode = t.crsCode AND c.deptId = @v8
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8)) as alias
WHERE s.id = alias.studId;
set profiling=0;
/*
# Query_ID, Duration, Query
'399', '0.00092375', 'SELECT s.name FROM Student s,\n	(SELECT t.studId\n	FROM Transcript t\n		JOIN Course c \n        ON c.crsCode = t.crsCode AND c.deptId = @v8\n		GROUP BY studId\n		HAVING COUNT(*) = \n			(SELECT COUNT(*) FROM Course WHERE deptId = @v8)) as alias\nWHERE s.id = alias.studId\nLIMIT 0, 50'
*/

DROP INDEX id_idx on Student;
DROP INDEX crsCode_idx on Transcript;
DROP INDEX deptID_idx on Course;
