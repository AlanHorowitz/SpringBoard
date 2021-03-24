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

-- 3. List the names of students who have taken course v4 (crsCode).
SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);

-- Bottleneck: Full scans on Student and Transcript
-- Found it by: checking whether index existed EXPLAIN shows type = ALL
-- Resolved by adding index on id column, index on crsCode
-- Rewrote query to use a JOIN instead of WHERE IN SELECT.   The execution plan for the JOIN was
-- simpler, but yielded similar results.

EXPLAIN SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'SIMPLE', '<subquery2>', NULL, 'ALL', NULL, NULL, NULL, NULL, NULL, '100.00', NULL
'1', 'SIMPLE', 'Student', NULL, 'ALL', NULL, NULL, NULL, NULL, '400', '10.00', 'Using where; Using join buffer (hash join)'
'2', 'MATERIALIZED', 'Transcript', NULL, 'ref', 'crsCode_semester_idx', 'crsCode_semester_idx', '1023', 'const', '2', '100.00', NULL
*/

SET profiling=1;
SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);
SET profiling=0;
/*
# Status, Duration, CPU_user, CPU_system
'executing', '0.000333', '0.000000', '0.000332'
*/

CREATE INDEX id_idx on Student (id);
CREATE INDEX crsCode_idx on Transcript (crsCode);

EXPLAIN SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'SIMPLE', '<subquery2>', NULL, 'ALL', NULL, NULL, NULL, NULL, NULL, '100.00', 'Using where'
'1', 'SIMPLE', 'Student', NULL, 'ref', 'id_idx', 'id_idx', '5', '<subquery2>.studId', '1', '100.00', NULL
'2', 'MATERIALIZED', 'Transcript', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'const', '2', '100.00', NULL
*/

SET profiling=1;
SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);
SET profiling=0;
/*
# Status, Duration, CPU_user, CPU_system
'executing', '0.000050', '0.000000', '0.000050'
*/

EXPLAIN SELECT DISTINCT name FROM Student s
JOIN Transcript t
ON s.id = t.studId AND crsCode = @v4;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'SIMPLE', 't', NULL, 'ref', 'crsCode_idx', 'crsCode_idx', '1023', 'const', '2', '100.00', 'Using where; Using temporary'
'1', 'SIMPLE', 's', NULL, 'ref', 'id_idx', 'id_idx', '5', 'springboardopt.t.studId', '1', '100.00', NULL
*/ 
-- Solution to problem 3

SET profiling=1;
SELECT DISTINCT name FROM Student s
JOIN Transcript t
ON s.id = t.studId AND crsCode = @v4;
SET profiling=0;
/*
# Status, Duration, CPU_user, CPU_system
'executing', '0.000048', '0.000000', '0.000047'
*/

DROP INDEX id_idx on Student;
DROP INDEX crsCode_idx on Transcript;
