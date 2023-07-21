README for SQLite3 Database Tool

Overview:
The SQLite3 Database Tool is an interactive tool that allows users to interface with their SQLite3 databases through a chat-like interface. The tool utilizes OpenAI's GPT-3 NLP engine to create an interactive experience, and features functions for executing SQL commands and displaying the contents of a database as an ASCII table. 

Requirements:
- Python 3.7 or higher
- OpenAI API key
- SQLite3 database file

Installation:
1. Clone the repository 
2. Install required packages with: 
    ```
    pip install requirements.txt
    ```
3. Create a `.env` file in the project directory containing your OpenAI API key:
    ```
    OpenAIKey=YOUR_API_KEY_HERE
    ```
4. Replace the default SQLite3 database file with your own database file. 

Usage:
1. Run the `mainmenuAI()` function to start the interface. 
2. Use the interface to execute SQL commands or display database contents as an ASCII table. 
3. To exit the program, use the `exit_program()` function call.

Functions:
1. `exit_program()` - Exits the program
2. `ReadDb(conn, c)` - Reads the database and displays contents as an ASCII table
3. `executer(conn, SqLc)` - Executes SQL commands on the database
4. `function_call(ai_response)` - Calls the specified function based on the user's input
5. `mainmenuAI(query)` - Main interface function that takes user input and generates a response using OpenAI's GPT-3 engine. 

Function Descriptions:
The `function_descriptions` array contains descriptions of the functions that are available for use through the interface. These descriptions are used by OpenAI's GPT-3 engine to generate more accurate responses. 

Note:
This tool is intended for educational and experimental purposes only. Use at your own risk.
