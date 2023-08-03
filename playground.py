import sqlite3

connection = sqlite3.connect('/Users/Pathompong/Documents/Projects/Python/myfinance/my_finance.db')
cursor = connection.cursor()

cursor.execute("""--sql
               SELECT ID from August
               ORDER by ID DESC
               """)
rows = cursor.fetchone()