SELECT 
    CASE 
        WHEN length < 60 THEN 'Short'
        WHEN length BETWEEN 60 AND 120 THEN 'Medium'
        ELSE 'Long'
    END AS length_bucket,
    COUNT(film_id) AS films
FROM 
    film
GROUP BY 
    1;
