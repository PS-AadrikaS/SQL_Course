SELECT 
    rating, 
    COUNT(film_id) AS film_count
FROM 
    film
GROUP BY 
    rating
ORDER BY 
    film_count DESC;
