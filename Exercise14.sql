
CREATE TEMP TABLE top_10_films AS
SELECT 
    f.title,
    COUNT(r.rental_id) AS rentals
FROM 
    film f
JOIN 
    inventory i ON f.film_id = i.film_id
JOIN 
    rental r ON i.inventory_id = r.inventory_id
GROUP BY 
    f.title
ORDER BY 
    rentals DESC
LIMIT 10;


SELECT 
    title, 
    rentals
FROM 
    top_10_films;
