SELECT 
    title, 
    rental_rate
FROM 
    film
WHERE 
    rental_rate > (SELECT AVG(rental_rate) FROM film)
ORDER BY 
    rental_rate DESC, 
    title ASC;
