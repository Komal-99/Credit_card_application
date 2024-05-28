import pandas as pd
import sqlite3
import os
folder_path='data_csv'
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        conn = sqlite3.connect('creditdata.db')
        df.to_sql(filename.split('.')[0], conn, if_exists='replace', index=False)
        conn.close()

conn = sqlite3.connect('creditdata.db')
data = pd.read_sql_query("SELECT * FROM sqlite_master;", conn)
print(data)

import sqlite3

def add_password_column(db_path='creditdata.db', default_password='Northcap@2024'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Add a new column 'password' with a default value
    cursor.execute(f"ALTER TABLE Users ADD COLUMN password TEXT DEFAULT '{default_password}'")
    conn.commit()
    conn.close()

add_password_column() 
