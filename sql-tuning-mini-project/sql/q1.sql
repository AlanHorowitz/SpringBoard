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

-- 1. List the name of the student with id equal to v1 (id).
SELECT name FROM Student WHERE id = @v1;

-- Bottleneck: Full scan being run to retrieve one row 
-- Found it by: Knowledge of indexing principles
-- Resolved by adding index on id column
--
-- Note: executing step improved 10x, though half runtime duration is common overhead. 

EXPLAIN SELECT name FROM Student WHERE id = @v1;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'SIMPLE', 'Student', NULL, 'ALL', NULL, NULL, NULL, NULL, '400', '10.00', 'Using where'
*/

set profiling=1;
SELECT name FROM Student WHERE id = @v1;
set profiling=0;
/*
# Status, Duration, CPU_user, CPU_system
'executing', '0.000247', '0.000000', '0.000246'
*/

CREATE INDEX id_idx on Student (id);
EXPLAIN SELECT name FROM Student WHERE id = @v1;
/*
# id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
'1', 'SIMPLE', 'Student', NULL, 'ref', 'id_idx', 'id_idx', '5', 'const', '1', '100.00', NULL
*/

set profiling=1;
SELECT name FROM Student WHERE id = @v1;
set profiling=0;
/*
# Status, Duration, CPU_user, CPU_system
'executing', '0.000026', '0.000000', '0.000026'
*/

DROP INDEX id_idx on Student;



