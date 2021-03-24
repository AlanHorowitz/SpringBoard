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

-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).
SELECT name FROM Student WHERE id BETWEEN @v2 AND @v3;

-- Bottleneck: No improvable bottleneck found.  Performance is better with	
-- table scan than going through an index.
--
-- execution time without index .00047 sec
-- execution time with (forced) index on id .00060 sec
-- (as reported by workbench duration)
