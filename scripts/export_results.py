import sqlite3
import pandas as pd
import os

# Get the absolute path of the project directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the database path
db_path = os.path.join(project_dir, 'analytics.db')

# Connect to SQLite database (create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL to create tables
create_tables_path = os.path.join(project_dir, 'scripts', 'create_tables.sql')
with open(create_tables_path, 'r') as file:
    create_tables_query = file.read()
cursor.executescript(create_tables_query)
conn.commit()

# Load the CSV data into the tables
sales_csv_path = os.path.join(project_dir, 'data', 'Sales.csv')
returns_csv_path = os.path.join(project_dir, 'data', 'Returns.csv')
sales_df = pd.read_csv(sales_csv_path)
returns_df = pd.read_csv(returns_csv_path)

sales_df.to_sql('Sales', conn, if_exists='replace', index=False)
returns_df.to_sql('Returns', conn, if_exists='replace', index=False)

# Define analysis queries
analysis_queries = {
    'sales_return_percentage': """
        SELECT 
            (COUNT(DISTINCT r.sale_id) * 100.0 / COUNT(DISTINCT s.sale_id)) AS return_percentage
        FROM 
            Sales s
        LEFT JOIN 
            Returns r ON s.sale_id = r.sale_id;
    """,
    'full_returns_percentage': """
        SELECT 
            (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Returns)) AS full_return_percentage
        FROM 
            Returns
        WHERE 
            return_amount = sale_amount;
    """,
    'average_return_percentage': """
        SELECT 
            AVG(return_amount * 100.0 / sale_amount) AS average_return_percentage
        FROM 
            Returns;
    """,
    'returns_within_7_days_percentage': """
        SELECT 
            (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Returns)) AS returns_within_7_days_percentage
        FROM 
            Returns r
        JOIN 
            Sales s ON r.sale_id = s.sale_id
        WHERE 
            julianday(r.return_date) - julianday(s.sale_date) <= 7;
    """,
    'average_days_for_return': """
        SELECT 
            AVG(julianday(r.return_date) - julianday(s.sale_date)) AS average_days_for_return
        FROM 
            Returns r
        JOIN 
            Sales s ON r.sale_id = s.sale_id;
    """,
    'most_valuable_customer': """
        SELECT 
            s.customer_id, 
            SUM(s.sale_amount) - IFNULL(SUM(r.return_amount), 0) AS net_sales
        FROM 
            Sales s
        LEFT JOIN 
            Returns r ON s.sale_id = r.sale_id
        GROUP BY 
            s.customer_id
        ORDER BY 
            net_sales DESC
        LIMIT 1;
    """
}

# Execute analysis queries and collect results
results = {}
for key, query in analysis_queries.items():
    cursor.execute(query)
    results[key] = cursor.fetchone()

# Close the database connection
conn.close()

# Process results into a DataFrame
results_df = pd.DataFrame([
    {'Metric': '% of sales resulting in a return', 'Value': results['sales_return_percentage'][0]},
    {'Metric': '% of returns that are full returns', 'Value': results['full_returns_percentage'][0]},
    {'Metric': 'Average return % amount', 'Value': results['average_return_percentage'][0]},
    {'Metric': '% of returns occurring within 7 days', 'Value': results['returns_within_7_days_percentage'][0]},
    {'Metric': 'Average number of days for a return', 'Value': results['average_days_for_return'][0]},
    {'Metric': 'Most valuable customer', 'Value': results['most_valuable_customer'][0]},
    {'Metric': 'Value of most valuable customer', 'Value': results['most_valuable_customer'][1]},
])

# Save the results to an Excel file
output_path = os.path.join(project_dir, 'output', 'Analysis_Results.xlsx')
results_df.to_excel(output_path, index=False)

print(f"Results have been exported to {output_path}")
