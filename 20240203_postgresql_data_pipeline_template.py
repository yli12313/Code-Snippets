"""
Description: Data pipeline connecting to PostgresSQL, reading from an existing table,
doing data preprocessing, and then writing to a new table.

Date: Sat. 2/3/24
"""
import pandas as pd
from sqlalchemy import create_engine

# Opening a PostgreSQL database connection.
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Read data from a SQL table.
df = pd.read_sql_table('mytable', engine)

# Mock data manipulations (modify when you need to):
# 1. Remove rows with missing values.
# 2. Creating a new column.
df = df.dropna()
df['new_column'] = df['column1'] + df['column2']

# Write the processed dataframe back to a new SQL table.
df.to_sql('processed_table', engine, if_exists='replace')
