-- Patient analytics queries for the Data Science Tool Mastery project (SQLite dialect)
-- Tables: patients(patient_id, age, sex_group, bmi, ..., target, bmi_band, age_group), bmi_bands(band, lower, upper, who_label)

-- name: highest_progression_obese_under_50
-- Obese patients younger than 50 with the highest disease progression
SELECT patient_id, age, bmi, target
FROM patients
WHERE bmi >= 30 AND age < 50
ORDER BY target DESC
LIMIT 5

-- name: band_summary
-- Summary per BMI band (GROUP BY + HAVING filters whole groups)
SELECT bmi_band,
       COUNT(*)                 AS patients,
       ROUND(AVG(target), 1)    AS mean_progression,
       MIN(target)              AS min_progression,
       MAX(target)              AS max_progression,
       ROUND(AVG(age), 1)       AS mean_age
FROM patients
GROUP BY bmi_band
HAVING COUNT(*) >= 20
ORDER BY mean_progression DESC

-- name: severity_levels
-- CASE turns a number into labelled categories
SELECT CASE WHEN target < 100 THEN '1 Low (<100)'
            WHEN target < 200 THEN '2 Medium (100-199)'
            ELSE                   '3 High (200+)' END AS severity,
       COUNT(*)              AS patients,
       ROUND(AVG(bmi), 1)    AS mean_bmi
FROM patients
GROUP BY severity
ORDER BY severity

-- name: join_with_lookup
-- JOIN with the lookup table to attach a readable label
SELECT b.who_label, COUNT(*) AS patients, ROUND(AVG(p.target), 1) AS mean_progression
FROM patients AS p
JOIN bmi_bands AS b ON p.bmi_band = b.band
GROUP BY b.who_label
ORDER BY mean_progression DESC

-- name: top2_per_band
-- CTE + window function: rank patients inside their own BMI band
WITH ranked AS (
    SELECT patient_id, bmi_band, target,
           RANK() OVER (PARTITION BY bmi_band ORDER BY target DESC) AS rnk,
           ROUND(AVG(target) OVER (PARTITION BY bmi_band), 1)        AS band_avg
    FROM patients
)
SELECT * FROM ranked WHERE rnk <= 2 ORDER BY bmi_band, rnk

-- name: bmi_quartiles
-- NTILE splits patients into equal-sized groups by BMI
SELECT quartile,
       COUNT(*)               AS patients,
       ROUND(MIN(bmi), 1)     AS min_bmi,
       ROUND(MAX(bmi), 1)     AS max_bmi,
       ROUND(AVG(target), 1)  AS mean_progression
FROM (SELECT bmi, target, NTILE(4) OVER (ORDER BY bmi) AS quartile FROM patients)
GROUP BY quartile
ORDER BY quartile

-- name: above_band_average
-- Correlated subquery: patients whose progression exceeds the average of their own band
SELECT COUNT(*) AS above_band_average
FROM patients AS p
WHERE target > (SELECT AVG(target) FROM patients WHERE bmi_band = p.bmi_band)

-- name: smoothed_progression
-- Moving average over a window of 29 neighbouring patients, ordered by BMI
SELECT patient_id, bmi, target,
       ROUND(AVG(target) OVER (ORDER BY bmi, patient_id ROWS BETWEEN 14 PRECEDING AND 14 FOLLOWING), 1) AS smoothed_progression
FROM patients
ORDER BY bmi, patient_id
