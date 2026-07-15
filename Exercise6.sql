SELECT 
    UPPER(first_name || ' ' || last_name) AS customer_name,
    SUBSTRING(email FROM POSITION('@' IN email) + 1) AS email_domain
FROM 
    customer;
