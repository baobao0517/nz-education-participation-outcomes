-- NZ Education Participation & Outcomes Insights
-- Tables are built from verified aggregate CSVs by src/verify_sql.py.
-- All analyses are descriptive; no student-level linkage or causal interpretation.

-- 1. Current performance and annual improvement, national vs each Regional Council.
WITH first_last AS (
    SELECT a.region, a.rate AS rate_2022, b.rate AS rate_2026,
           b.gap AS gap_2026_pp
    FROM attendance a
    JOIN attendance b ON a.region = b.region
    WHERE a.year = 2022 AND b.year = 2026
)
SELECT region, rate_2022, rate_2026, gap_2026_pp,
       ROUND((rate_2026 - rate_2022) / 4.0, 3) AS annual_improvement_pp_per_year
FROM first_last
ORDER BY rate_2026 ASC;

-- 2. Persistent school-leaver attainment gaps use each year's NZ benchmark.
SELECT region,
       SUM(CASE WHEN gap < 0 THEN 1 ELSE 0 END) AS below_nz_years_2019_2025,
       ROUND(AVG(gap), 2) AS mean_annual_gap_pp,
       MAX(CASE WHEN year = 2025 THEN rate END) AS ncea_l2_2025_pct
FROM ncea
GROUP BY region
ORDER BY below_nz_years_2019_2025 DESC, mean_annual_gap_pp ASC;

-- 3. One-to-one 2025 ecological comparison of attendance and school-leaver attainment.
WITH pairs AS (
    SELECT a.region, a.rate AS attendance_2025, a.gap AS attendance_gap_pp,
           n.rate AS ncea_l2_2025, n.gap AS ncea_gap_pp
    FROM attendance a
    JOIN ncea n ON n.region = a.region AND n.year = a.year
    WHERE a.year = 2025
)
SELECT region, attendance_2025, ncea_l2_2025, attendance_gap_pp, ncea_gap_pp,
       CASE WHEN attendance_gap_pp < 0 AND ncea_gap_pp < 0 THEN 'Dual gap'
            WHEN attendance_gap_pp > 0 AND ncea_gap_pp > 0 THEN 'Both above'
            WHEN attendance_gap_pp * ncea_gap_pp < 0 THEN 'Mismatch'
            ELSE 'On benchmark' END AS descriptive_quadrant
FROM pairs
ORDER BY ncea_gap_pp ASC;

-- 4. 2025 region-within-EQI-group attainment vs SAME-group pooled 16-region rate.
--    Suppress n<30 in public interactive view; leave detail in reproducibility exports.
SELECT region, grp, n AS leavers, ROUND(rate, 1) AS pct_l2_plus,
       ROUND(pooledRate, 1) AS pooled_same_eqi_group_pct,
       ROUND(differencePp, 2) AS gap_vs_pooled_group_pp
FROM subgroups
WHERE dimension = 'eqi' AND n >= 30
ORDER BY region, grp;
