
import os
from dotenv import load_dotenv
import sqlite3
import openai
import json
import sys
import platform

#----------------------------------------------------------------------------------------------------------------------------------------------------

load_dotenv()                                                                                           
openai.api_key = os.getenv('OpenAIKey')
conn = sqlite3.connect('database.db')
c = conn.cursor()

#----------------------------------------------------------------------------------------------------------------------------------------------------

def exit_program():
    print("Exiting...")
    sys.exit()

#----------------------------------------------------------------------------------------------------------------------------------------------------

def clear_screen():

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

#----------------------------------------------------------------------------------------------------------------------------------------------------

def ReadDb(conn, c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    data = {}

    for table in tables:
        table_name = table[0]
        c.execute(f"SELECT * FROM [{table_name}];")
        rows = c.fetchall()

        table_data = []
        for row in rows:
            row_data = {}
            for i, column in enumerate(c.description):
                column_name = column[0]
                row_data[column_name] = row[i]
            
            table_data.append(row_data)

        data[table_name] = {
            "table_name": table_name,
            "columns": [column[0] for column in c.description],
            "data": table_data
        }
    
    return json.dumps(data, indent=4)

#----------------------------------------------------------------------------------------------------------------------------------------------------

def executer(conn, SqLc):
    try:
        c = conn.cursor()
        c.execute(SqLc)
        conn.commit()
        message = "Success"
        status = "success"
    except sqlite3.Error as e:
        message = f'Error: {str(e)}'
        status = "error"

    response_dict = {
        "status": status,
        "message": message,
        "executed_command": SqLc
    }

    return json.dumps(response_dict)

#----------------------------------------------------------------------------------------------------------------------------------------------------

function_descriptions = [
    {
        "name": "Commands",
        "description": "Triggered when the user wants to make modifications to data in the database.{Do not execute when wanting to look at the database}",
        "parameters": {
            "type": "object",
            "properties": {
                "Comm_and": {
                    "type": "string",
                    "description": "This is an Enviroment where you execute sql commands directly: convert user input to actual sql command."
                },
            },
            "required": ["Comm_and"]
        }
    },
    {
        "name": "read_db",
        "description": "Display, Show, Tell Me about the database. Display the database content in ASCII Table format.",
        "parameters": {
            "type": "object",
            "properties": {}}
    },
    {
        "name": "exit_program",
        "description": "Exits or quits the program",
        "parameters": {
            "type": "object",
            "properties": {}}
    }
]

#----------------------------------------------------------------------------------------------------------------------------------------------------

def function_call(ai_response):
    function_call = ai_response["choices"][0]["message"]["function_call"]
    function_name = function_call["name"]
    arguments = function_call["arguments"]
    
    if function_name == "Commands":
        query = eval(arguments).get("Comm_and")
        print("\nTriggered " + str(query))
        outcome = executer(conn, query)
    
        return outcome
    
    if function_name == "read_db":
        outcome = ReadDb(conn,c)
        return outcome
    
    if function_name == "exit_program":
        exit_program()
        return
    
    else:
        return

def mainmenuAI(query):
    messages = [
        {"role": "system", "content": "You are an SQLite3 Database interface. Restrict all conversation database related. Database should always be displayed as an ASCII table.\nThis is the current database.\n" + ReadDb(conn,c)},
        {"role": "user", "content": query}
    ]
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions = function_descriptions,
    function_call="auto"
    )

    while response["choices"][0]["finish_reason"] == "function_call":
        function_response = function_call(response)
        messages.append({
            "role": "function",
            "name": response["choices"][0]["message"]["function_call"]["name"],
            "content": json.dumps(function_response)
        })
        
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                functions = function_descriptions,
                function_call="auto"
        )
        
        if response['choices'][0]['message']['content'] is not None:
            content = response['choices'][0]['message']['content'].strip()
        else:
            pass
    else:
        print("\n"+response['choices'][0]['message']['content'].strip())


while True:
    user_input = input("Welcome to the SQLite3 Database Tool: ")
    mainmenuAI(user_input)
    clear_screen


#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    mainmenuAI()
