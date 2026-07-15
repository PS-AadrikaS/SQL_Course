SELECT 
    first_name, 
    last_name, 
    'Actor' AS type
FROM 
    actor

UNION ALL

SELECT 
    first_name, 
    last_name, 
    'Staff' AS type
FROM 
    staff;
