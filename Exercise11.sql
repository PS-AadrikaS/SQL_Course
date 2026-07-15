WITH film_rental_counts AS (
    SELECT 
        c.name AS category,
        f.title,
        COUNT(r.rental_id) AS rentals
    FROM 
        category c
    JOIN 
        film_category fc ON c.category_id = fc.category_id
    JOIN 
        film f ON fc.film_id = f.film_id
    JOIN 
        inventory i ON f.film_id = i.film_id
    JOIN 
        rental r ON i.inventory_id = r.inventory_id
    GROUP BY 
        c.name, f.title
)
SELECT 
    category,
    title,
    rentals,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY rentals DESC) AS rnk
FROM 
    film_rental_counts;
