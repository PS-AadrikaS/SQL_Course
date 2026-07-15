# SQL Kickstart Course Exercises

This repository contains my completed exercises and automation project for the **SQL Kickstart** course. 

The project connects to a PostgreSQL `dvdrental` database, runs 14 distinct SQL assignments, and automatically compiles the results into a clean Excel workbook.

## What is Included
* `exercises 1 to 14` - My SQL script containing all 14 course queries (covering Joins, CTEs, Window Functions, Views, and Temp Tables).
* `Exercise15.py` - A Python script that automatically runs the queries and exports the data.
* `requirements.txt` - The Python libraries needed to run the automation pipeline.



## How to Run the Script
1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Update your database password inside `automate_exercises.py`.
3. Run the automation pipeline:
   ```bash
   python automate_exercises.py
   ```
