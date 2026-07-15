WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        SUM(p.amount) AS total_spent
    FROM 
        customer c
    JOIN 
        payment p ON c.customer_id = p.customer_id
    GROUP BY 
        c.customer_id, c.first_name, c.last_name
)
SELECT 
    customer_name, 
    total_spent
FROM 
    customer_spending
WHERE 
    total_spent > (SELECT AVG(total_spent) FROM customer_spending)
ORDER BY 
    total_spent DESC;
