import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

# 1. Database Connection Configuration
# Adjust user, password, host, and port to match your local PostgreSQL setup
DB_USER = "postgres"
DB_PASS = "your_password"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dvdrental"

# Create a SQLAlchemy engine for Pandas integration
conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_string)

# 2. Dictionary mapping each sheet name to its respective SQL execution blocks
# For structural questions (M-Views, Views, Temp Tables), we run setup blocks first.
queries = {
    "Q1": "SELECT title AS \"Film Title\", rental_rate AS \"Daily Price\" FROM film ORDER BY title ASC LIMIT 10;",
    "Q2": "SELECT title, length FROM film WHERE title LIKE 'A%' AND length BETWEEN 60 AND 120 ORDER BY length ASC;",
    "Q3": "SELECT rating, COUNT(film_id) AS film_count FROM film GROUP BY rating ORDER BY film_count DESC;",
    "Q4": "SELECT c.name AS category, COUNT(fc.film_id) AS film_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id GROUP BY c.name HAVING COUNT(fc.film_id) > 65 ORDER BY film_count DESC;",
    "Q5": "SELECT f.title, c.name AS category FROM film f INNER JOIN film_category fc ON f.film_id = fc.film_id INNER JOIN category c ON fc.category_id = c.category_id ORDER BY category ASC, title ASC;",
    "Q6": "SELECT UPPER(first_name || ' ' || last_name) AS customer_name, SUBSTRING(email FROM POSITION('@' IN email) + 1) AS email_domain FROM customer;",
    "Q7": "SELECT first_name, last_name, 'Actor' AS type FROM actor UNION ALL SELECT first_name, last_name, 'Staff' AS type FROM staff;",
    "Q8": "SELECT CASE WHEN length < 60 THEN 'Short' WHEN length BETWEEN 60 AND 120 THEN 'Medium' ELSE 'Long' END AS length_bucket, COUNT(film_id) AS films FROM film GROUP BY 1;",
    "Q9": "WITH customer_spending AS (SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name, SUM(p.amount) AS total_spent FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id, c.first_name, c.last_name) SELECT customer_name, total_spent FROM customer_spending WHERE total_spent > (SELECT AVG(total_spent) FROM customer_spending) ORDER BY total_spent DESC;",
    "Q10": "SELECT title, rental_rate FROM film WHERE rental_rate > (SELECT AVG(rental_rate) FROM film) ORDER BY rental_rate DESC, title ASC;",
    "Q11": "WITH film_rental_counts AS (SELECT c.name AS category, f.title, COUNT(r.rental_id) AS rentals FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN film f ON fc.film_id = f.film_id JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY c.name, f.title) SELECT category, title, rentals, DENSE_RANK() OVER (PARTITION BY category ORDER BY rentals DESC) AS rnk FROM film_rental_counts;",
    
    # Q12: Build/Replace view first, then query the virtual object
    "Q12_SETUP": "CREATE OR REPLACE VIEW film_catalog AS SELECT f.title, c.name AS category, f.rental_rate, f.length FROM film f INNER JOIN film_category fc ON f.film_id = fc.film_id INNER JOIN category c ON fc.category_id = c.category_id;",
    "Q12": "SELECT title, rental_rate, length FROM film_catalog WHERE category = 'Comedy' ORDER BY title ASC;",
    
    # Q13: Build/Refresh Materialized view first, then extract reporting metrics
    "Q13_SETUP": "DROP MATERIALIZED VIEW IF EXISTS category_revenue; CREATE MATERIALIZED VIEW category_revenue AS SELECT c.name AS category, SUM(p.amount) AS revenue FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN inventory i ON fc.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id JOIN payment p ON r.rental_id = p.rental_id GROUP BY c.name; REFRESH MATERIALIZED VIEW category_revenue;",
    "Q13": "SELECT category, revenue FROM category_revenue ORDER BY revenue DESC LIMIT 5;",
    
    # Q14: Spin up transactional session memory scratchpad, then pull final shortlist
    "Q14_SETUP": "CREATE TEMP TABLE top_10_films AS SELECT f.title, COUNT(r.rental_id) AS rentals FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY f.title ORDER BY rentals DESC LIMIT 10;",
    "Q14": "SELECT title, rentals FROM top_10_films;"
}

output_file = "sql_exercise_outputs.xlsx"

# 3. Execution Pipeline and Excel Compiling Process
print("🚀 Starting automated SQL workbook compiler pipeline...")

try:
    # Initialize the high-level Excel output engine 
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:

        
        # Connect directly via psycopg2 connection wrapper to run setups + temp tables seamlessly
        with engine.connect() as connection:
            
            # Since Q14 Temp Table lives strictly inside ONE transaction session,
            # we use a persistent transaction block to execute setup statements.
            trans = connection.begin()
            try:
                # Pre-run required setup items to build views/tables safely
                # Pre-run required setup items to build views/tables safely
                for setup_key in ["Q12_SETUP", "Q13_SETUP", "Q14_SETUP"]:
                    connection.execute(text(queries[setup_key]))

                
                # Fetch and export structured queries to targeted sheets
                for q_num in range(1, 15):
                    sheet_name = f"Q{q_num}"
                    sql_query = queries[sheet_name]
                    
                    print(f"📊 Compiling dataset sheet: {sheet_name}...")
                    
                    # Feed database records straight into a Pandas DataFrame
                    df = pd.read_sql_query(text(sql_query), connection)

                    
                    # Write rows into dedicated target Excel tab
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                trans.commit() # Commit transaction actions
                print(f"🎉 Success! Complete compilation saved to file: '{output_file}'")
                
            except Exception as e:
                trans.rollback() # Rollback changes safely if it breaks
                raise e

except Exception as err:
    print(f"❌ Critical Pipeline Failure: {err}")
