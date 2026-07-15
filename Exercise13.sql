CREATE MATERIALIZED VIEW category_revenue AS
SELECT 
    c.name AS category,
    SUM(p.amount) AS revenue
FROM 
    category c
JOIN 
    film_category fc ON c.category_id = fc.category_id
JOIN 
    inventory i ON fc.film_id = i.film_id
JOIN 
    rental r ON i.inventory_id = r.inventory_id
JOIN 
    payment p ON r.rental_id = p.rental_id
GROUP BY 
    c.name;


SELECT 
    category, 
    revenue
FROM 
    category_revenue
ORDER BY 
    revenue DESC
LIMIT 5;


REFRESH MATERIALIZED VIEW category_revenue;