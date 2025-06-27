-- Query 1: Average programming performance per batch
SELECT s.course_batch, AVG(p.problems_solved) as avg_problems_solved
FROM students s
JOIN programming p ON s.student_id = p.student_id
GROUP BY s.course_batch;

-- Query 2: Top 5 students ready for placement
SELECT s.name, p.latest_project_score, pl.mock_interview_score
FROM students s
JOIN programming p ON s.student_id = p.student_id
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Ready'
ORDER BY p.latest_project_score DESC, pl.mock_interview_score DESC
LIMIT 5;

-- Query 3: Distribution of soft skills scores
SELECT 
    CASE 
        WHEN communication >= 90 THEN '90-100'
        WHEN communication >= 80 THEN '80-89'
        WHEN communication >= 70 THEN '70-79'
        ELSE 'Below 70'
    END as communication_score_range,
    COUNT(*) as count
FROM soft_skills
GROUP BY communication_score_range;

-- Query 4: Students with multiple internships
SELECT s.name, pl.internships_completed
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.internships_completed > 1
ORDER BY pl.internships_completed DESC;

-- Query 5: Average placement package by city
SELECT s.city, AVG(pl.placement_package) as avg_package
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Placed'
GROUP BY s.city;

-- Query 6: Students with high soft skills scores
SELECT s.name, AVG(ss.communication + ss.teamwork + ss.presentation) as avg_soft_skills
FROM students s
JOIN soft_skills ss ON s.student_id = ss.student_id
GROUP BY s.student_id, s.name
HAVING avg_soft_skills > 85
ORDER BY avg_soft_skills DESC;

-- Query 7: Programming language preference
SELECT p.language, COUNT(*) as student_count
FROM programming p
GROUP BY p.language;

-- Query 8: Placement success rate by batch
SELECT s.course_batch, 
       COUNT(CASE WHEN pl.placement_status = 'Placed' THEN 1 END) * 100.0 / COUNT(*) as success_rate
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
GROUP BY s.course_batch;

-- Query 9: Students with certifications
SELECT s.name, p.certifications_earned
FROM students s
JOIN programming p ON s.student_id = p.student_id
WHERE p.certifications_earned > 0
ORDER BY p.certifications_earned DESC;

-- Query 10: Recent placements
SELECT s.name, pl.company_name, DATE_FORMAT(pl.placement_date, '%Y-%m-%d') as placement_date
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Placed'
ORDER BY pl.placement_date DESC
LIMIT 10;