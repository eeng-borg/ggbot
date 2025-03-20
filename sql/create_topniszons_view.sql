DROP VIEW IF EXISTS korniszons_test_topniszon;
CREATE VIEW korniszons_test_topniszon AS
WITH RankedInputs AS (
    -- Rank inputs within each day based on score
    SELECT 
        DATE(created) as date,
        id,
        input,
        user,
        score,
        created,
        ROW_NUMBER() OVER (
            PARTITION BY DATE(created) 
            ORDER BY score DESC, created ASC
        ) AS daily_rank
    FROM korniszons_test
),
GlobalRanking AS (
    -- Calculate global position for all inputs
    SELECT 
        id,
        ROW_NUMBER() OVER (
            ORDER BY score DESC, created ASC
        ) AS position
    FROM korniszons_test
)
-- Select only the best input for each day
SELECT 
    r.date,
    r.input,
    r.user,
    r.score,
    r.created,
    g.position
FROM RankedInputs r
JOIN GlobalRanking g ON r.id = g.id
WHERE r.daily_rank = 1
ORDER BY r.date DESC;