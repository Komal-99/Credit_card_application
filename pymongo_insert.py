# Get the database using the method we defined in pymongo_test_insert file
from Text_to_sql.streamlit_application.pymongo_get_database import get_database
import pandas as pd
import os 
import csv
dbname = get_database()
# Establising a connection with mongoDB on cloudbased server.

print(dbname)
# we have created a database but still it is not present, reason is till the time we will not create a collection, the dabase will not be present\\.)

# let's verify whether we have our collaction name in the database or not 
# we'll use the following function:-

def checkExistence_COL(COLLECTION_NAME, DB_NAME, db):
    """It verifies the existence of collection name in a database"""
    collection_list = db.list_collection_names()
    
    if COLLECTION_NAME in collection_list:
        print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' exists")
        return True
    
    print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' does not exists OR \n\
    no documents are present in the collection")
    return False


_ = checkExistence_COL(COLLECTION_NAME="Credit_data", DB_NAME="CreditData", db=dbname)
folder_path = "data_csv"
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df=pd.read_csv(file_path)
        data=df.to_dict(orient="records")
        print(data)
        collection_name = dbname[filename.split(".")[0]]
        collection_name.insert_many(data)