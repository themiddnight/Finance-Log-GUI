import sqlite3
from datetime import datetime

connection = sqlite3.connect('/Users/Pathompong/Documents/Projects/Python/myfinance/my_finance.db')
cursor = connection.cursor()

# prepare variable
table  = datetime.now().strftime('%B')
date   = datetime.now().strftime('%d/%m/%y')
bank   = 3789
wallet = 1680

# check if it has the table
cursor.execute("""--sql
               SELECT ID from {};
               """.format(table))
if not cursor.fetchone():
    cursor.execute("""--sql
                   CREATE TABLE {} 
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                   date TEXT, bank NUMERIC, wallet NUMERIC, 
                   bank_dif NUMERIC, wallet_dif NUMERIC, total_dif NUMERIC);
                   """.format(table))
	
# read table - check latest id
cursor.execute("""--sql
               SELECT ID from {}
               ORDER by ID DESC
               """.format(table))
rows = cursor.fetchone()[0]
if not rows: id = 0     # if empty, start with 0
else: id = rows + 1     # if has data, increase id

# add item to table
cursor.execute("""--sql
               INSERT INTO {} (ID, date, bank, wallet)
               VALUES ({}, '{}', {}, {});
               """.format(table, id, date, bank, wallet))
connection.commit()

# update difference value to table
cursor.execute("""--sql
               SELECT bank, wallet FROM {}
               ORDER by ID DESC
               """.format(table))
rows = cursor.fetchmany(2)  # get 2 latest row
if len(rows) == 2:          # if it has 2 rows that can find difference
    bank_dif   = rows[0][0] - rows[1][0]
    wallet_dif = rows[0][1] - rows[1][1]
    total_dif  = bank_dif + wallet_dif
    cursor.execute("""--sql
                   UPDATE {} 
                   SET bank_dif = {}, wallet_dif = {}, total_dif = {}
                   WHERE ID = {}
                   """.format(table, bank_dif, wallet_dif, total_dif, id))
connection.commit()

# get sum of each differences
cursor.execute("""--sql
               SELECT SUM(bank_dif), SUM(wallet_dif), SUM(total_dif) FROM {}
               """.format(table))
rows = cursor.fetchall()
print('=====================================')
print('Total bank spending:   ', rows[0][0], 'THB')
print('Total wallet spending: ', rows[0][1], 'THB')
print('-------------------------------------')
print('Total spending:        ', rows[0][2], 'THB')
print('=====================================')

cursor.close()
connection.close()