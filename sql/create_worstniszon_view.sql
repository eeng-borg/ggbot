DROP VIEW IF EXISTS korniszons_test_worstniszon;
CREATE VIEW korniszons_test_worstniszon AS
WITH RankedInputs AS (
    -- Rank inputs within each day based on score (ascending for worst)
    SELECT 
        DATE(created) as date,
        id,
        input,
        user,
        score,
        created,
        ROW_NUMBER() OVER (
            PARTITION BY DATE(created) 
            ORDER BY score ASC, created DESC  -- Changed to ASC for worst scores
        ) AS daily_rank
    FROM korniszons_test
    WHERE score > 0  -- Only include scores above 0
),
GlobalRanking AS (
    -- Calculate global position for all inputs (keeps original DESC order)
    SELECT 
        id,
        ROW_NUMBER() OVER (
            ORDER BY score DESC, created ASC
        ) AS position
    FROM korniszons_test
    WHERE score > 0
)
-- Select only the worst input for each day
SELECT 
    r.date,
    r.input,
    r.user,
    r.score,
    r.created,
    g.position
FROM RankedInputs r
JOIN GlobalRanking g ON r.id = g.id
WHERE r.daily_rank = 1  -- Gets the worst score for each day
ORDER BY r.date DESC;