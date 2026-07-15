SELECT 
    f.title, 
    c.name AS category
FROM 
    film f
INNER JOIN 
    film_category fc ON f.film_id = fc.film_id
INNER JOIN 
    category c ON fc.category_id = c.category_id
ORDER BY 
    category ASC, 
    title ASC;
