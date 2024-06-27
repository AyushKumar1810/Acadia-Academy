# SQL Analysis Project

## Project Structure

ACADIA ACADMY/
│
├── data/
│ ├── Sales.csv
│ ├── Returns.csv
│
├── scripts/
│ ├── create_tables.sql
│ ├── import_data.sql
│ ├── analysis_queries.sql
│ ├── export_results.py
│
├── output/
│ └── Analysis_Results.xlsx
│
├── README.md
└── .env

## Steps to Run the Project

1. **Create the Database and Tables:**

   ```bash
   sqlite3 ACADIA ACADMY/analytics.db < ACADIA ACADMY/scripts/create_tables.sql
<!-- Import Data into the Tables:


sqlite3 ACADIA ACADMY/analytics.db < ACADIA ACADMY/scripts/import_data.sql

*Execute Analysis Queries and Export Results:

python ACADIA ACADMY/scripts/export_results.py -->

## View the Results:
```   Open the Analysis_Results.xlsx file in the output folder.

<!-- Requirements
* SQLite
* Python 3.x
* pandas
* openpyxl -->

<!-- Notes
*Ensure the CSV files are correctly placed in the data folder.
*Ensure you have the required Python packages installed. -->
