import sqlite3

def login(email, password, db_path='creditdata.db'):
    print("Email:", email)
    print("Password:", password)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'SELECT password FROM Users WHERE Email = ?'

    # Print the query for debugging
    print("Executing SQL query:", query, "with parameters:", (email,))

    cursor.execute(query, (email,))
    result = cursor.fetchone()

    # Print the query result for debugging
    print("Query result:", result)

    conn.close()

    if result and result[0] == password:
        return True
    else:
            return False
def register(name, age, email, city, card_type, credit_limit, company, job_segment, password, db_path='creditdata.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Query to fetch the highest customer_id
        cursor.execute("SELECT customer_id FROM Users ORDER BY CAST(SUBSTR(customer_id, 2) AS INTEGER) DESC LIMIT 1")
        last_customer_id = cursor.fetchone()

        # Calculate the next customer_id
        if last_customer_id:
            # Extract the numeric part and increment it
            last_id_number = int(last_customer_id[0][1:])  # Strip the leading 'A' and convert to integer
            new_customer_id = 'A' + str(last_id_number + 1)
        else:
            # If there are no users, start from A1
            new_customer_id = 'A1'

        # SQL query to insert a new user
        query = """
        INSERT INTO Users (customer_id, Name, age, Email, city, card_type, credit_limit, company, job_segment, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (new_customer_id, name, age, email, city, card_type, credit_limit, company, job_segment, password)

        # Execute the query
        cursor.execute(query, parameters)

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return False
    finally:
        # Ensure the database connection is closed
        conn.close()

    return True

# Example usage: