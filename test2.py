import psycopg2

# Connect to your PostgreSQL database

conn = psycopg2.connect(

    database="user_service",  # Replace with your actual database name    
    host= "xxxx.rds.amazonaws.com",
password = "",
user = "postgres",
)

cur = conn.cursor()

# Fetch all tables and their columns
cur.execute("""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'public' AND data_type IN ('character varying', 'text');
""")

tables_columns = cur.fetchall()

search_string = '.us-east-1' #string to check

# Loop through tables and columns to find the search string
for table_name, column_name in tables_columns:
    cur.execute(f"SELECT * FROM {table_name} WHERE {column_name} = %s", (search_string,))
    rows = cur.fetchall()
    if rows:
        print(f"Found in {table_name}.{column_name}: {rows}")

# Clean up
cur.close()
conn.close()

