CREATE OR REPLACE VIEW film_catalog AS
SELECT 
    f.title, 
    c.name AS category, 
    f.rental_rate, 
    f.length
FROM 
    film f
INNER JOIN 
    film_category fc ON f.film_id = fc.film_id
INNER JOIN 
    category c ON fc.category_id = c.category_id;

SELECT 
    title, 
    rental_rate, 
    length
FROM 
    film_catalog
WHERE 
    category = 'Comedy'
ORDER BY 
    title ASC;