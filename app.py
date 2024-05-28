
import os
import pandas as pd
import sqlite3
import google.generativeai as genai
from flask_cors import CORS
from flask import request,Flask
from flask import jsonify
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from RSAEncryption import enc

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyB-yonXYg46BDnEahFHy_0ZSi0BwLNnI-w")

## Define Your Prompt
prompt=[
    """
You're working with a SQL database called "creditdata" which consists of three tables:

CREATE TABLE "repayment" (
  "customer_id" TEXT,
  "date" TEXT,
  "amount" REAL
)

CREATE TABLE "spend" (
  "customer_id" TEXT,
  "date" TEXT,
  "product_type" TEXT,
  "amount" REAL
)

CREATE TABLE "Users" (
  "num" INTEGER,
  "customer_id" TEXT,
  "Name" TEXT,
  "age" INTEGER,
  "Email" TEXT,
  "city" TEXT,
  "card_type" TEXT,
  "credit_limit" INTEGER,
  "company" TEXT,
  "job_segment" TEXT
  "password" TEXT
)
Note : - You are not allowed to do any delete or alter operations on the database. or sum  direclty retrive data and answer the question as it is.
Users can inquire about their credit card transactions and repayment status using SQL queries. For example:
- Example 1: Retrieve spend analysis of user A1 for January?, 
    the SQL command will be something like this SELECT * FROM spend WHERE customer_id='A1' AND strftime('%Y-%m', date)='2004-01';
- Example 2: Inquire about the expenditure of user A2 in the year 2004? , 
    the SQL command will be something like this SELECT SUM(amount) FROM spend WHERE customer_id='A2' AND strftime('%Y', date)='2004';
- Example 3: Fetch details on when user A2 repaid their amount in April and how much? , 
    the SQL command will be something like this SELECT date, amount FROM repayment WHERE customer_id='A2' AND strftime('%Y-%m', date)='2004-04';

Please note that if the model is unable to provide an answer, it will respond with "Not able to predict." also the sql code should not have ``` in beginning or end and sql word in output. 

    """

]
model=genai.GenerativeModel('gemini-pro')
def get_gemini_response(question,prompt):
    response=model.generate_content([prompt[0],question])
    # response=model(prompt[0]+question)[0]['generated_text']
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt2 = PromptTemplate.from_template(
    template="You are a credit card expense manager expert managing money in indian ruppees (Rs.) and you will be question and its sql fetched output on expenses done by user or repayment dates. User can also ask you some general advice regarding expense management and how  to save money. Your role is to first summarize the sql data based on what is asked in question in a friendly tone as a advisor and expense mamanger and answer users queries.\n your question is {data}.\n Don't return Sql code in output and question. Directly give short answer and format in string no need to use astricks in fields. Answer should be short and precise.",
    
)

llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3) # set the convert_system_message_to_human to true 
def chain(question,answer,prompt2):
    ch=LLMChain(llm=llm,prompt=prompt2,verbose=True)
    text= question + "and answer is" + str(answer)
    response = ch.invoke(input=text)
    return response


@app.route('/credit_bot', methods=['POST'])
def hello_http():
    if request.is_json:
        # Retrieve JSON data from the request body
        json_data = request.get_json()
        
        # Check if the 'string' parameter exists in the JSON data
        if 'ques' in json_data:
            string_value = json_data['ques']
            print(string_value)
            # Process the received string with your qa_chain
            res=get_gemini_response(string_value,prompt)
            print(res)
            response=read_sql_query(res,"creditdata.db")
            ans=chain(string_value,response,prompt2)
            print(ans)
            # Return the answer in a JSON response
            print(type(ans['text']))
            return jsonify({"answer": ans['text']})
            # return jsonify({"answer": ans.content})
        else:
            return jsonify({"error": "'string' parameter not found in JSON data"}), 400
    else:
        return jsonify({"error": "Request must contain JSON"}),400

# Function to get the start and end dates of the quarter
def get_quarter_dates(quarter,year=2004):
    year=2004
    print(quarter,year)
    if quarter == 1:
        start_date = f"{year}-01-01"
        end_date = f"{year}-03-31"
    elif quarter == 2:
        start_date = f"{year}-04-01"
        end_date = f"{year}-06-30"
    elif quarter == 3:
        start_date = f"{year}-07-01"
        end_date = f"{year}-09-30"
    elif quarter == 4:
        start_date = f"{year}-10-01"
        end_date = f"{year}-12-31"
    else:
        raise ValueError("Quarter must be between 1 and 4")
    return start_date, end_date

@app.route('/get_user_spend', methods=['GET'])
def get_user_spend():
    # Get parameters from the request
    json_data = request.get_json()
    if "user_id" in json_data and "quarter" in json_data:
        id=json_data['user_id']
        quarter= json_data['quarter']
        print(id,quarter)
        if 1 <= quarter <= 4:
            start_date, end_date = get_quarter_dates(quarter,2004)
            print("called get_quarter_dates")
            # Connect to the SQLite database
            conn = sqlite3.connect('creditdata.db')
            cursor = conn.cursor()

            # SQL query to fetch user spend data
            query = """
            SELECT * FROM spend
            WHERE customer_id = (
                SELECT customer_id
                FROM Users
                WHERE Email = ?
            )
            AND strftime('%Y-%m', date) BETWEEN ? AND ?
            """
            cursor.execute(query, (id, start_date, end_date))
            
            # Fetch the results
            rows = cursor.fetchall()
            conn.close()

            # Convert the results to a list of dictionaries
            spend_data = []
        
            for row in rows:
                spend_data.append({
                    "Id": row[0],
                    "date": row[1],
                    "Product_type": row[2],
                    "Amount": row[3]
                })

            # Return the data as a JSON object
            return jsonify(spend_data)
        else:
            return jsonify({"error": "Quarter must be between 1 and 4"}), 400
    else:
        return jsonify({"error": "User_id and quarter are required parameters"}), 400
@app.route('/process_file', methods=['POST'])
def process_file():
    # Get the filename from the request JSON
    json_data = request.get_json()
    if "filename" in json_data:
        filename = json_data['filename']
        print(filename)
        # Construct the file path
        file_path = os.path.join('uploaded_images', filename['path'])
        print(file_path)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Call the enc function with the file path
        encoded_data = enc(image_path=file_path)
        
        # Return the encoded data as JSON
        return encoded_data
    else:
        return jsonify({"error": "Filename is a required parameter"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)

