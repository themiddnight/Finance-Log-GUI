import sqlite3
import json
from datetime import datetime

# prepare variable
income = 200
bank   = 5786
wallet = 1600
table  = datetime.now().strftime('%B_%Y')
date   = datetime.now().strftime('%d/%m/%y')
with open('data/path.json', 'r') as f:
    connection_path = json.load(f)['0']

def insert_data(table, date, income, bank, wallet):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()

    # check if it has the table
    try:
        cursor.execute("""--sql
                    SELECT ID from {};
                    """.format(table))
    except:
        cursor.execute("""--sql
                    CREATE TABLE {} 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, wallet NUMERIC, 
                    bank_dif NUMERIC, wallet_dif NUMERIC, total_dif NUMERIC);
                    """.format(table))
        
    # read 2 latest row
    cursor.execute("""--sql
                SELECT ID, bank, wallet FROM {}
                ORDER by ID DESC
                """.format(table))
    rows = cursor.fetchmany(2)

    # check latest id
    if not rows: id = 0         # if empty, start with 0
    else: id = rows[0][0] + 1   # if has data, increase id

    # calculate difference
    if len(rows) >= 1:          # if it has a row prior to find difference
        if not income:
            bank_dif   = (bank - rows[0][1])
        else:
            bank_dif   = (bank - rows[0][1]) - income
        wallet_dif = wallet - rows[0][2]
        total_dif  = bank_dif + wallet_dif
    else:
        bank_dif   = None
        wallet_dif = None
        total_dif  = None

    # add item to table
    cursor.execute("""--sql
                   INSERT INTO {} (ID, date, income, bank, wallet, bank_dif, wallet_dif, total_dif)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                   """.format(table), (id, date, income, bank, wallet, bank_dif, wallet_dif, total_dif))
    connection.commit()

    cursor.close()
    connection.close()

def show_sum():
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()

    # get sum of each differences
    cursor.execute("""--sql
                   SELECT SUM(income), SUM(bank_dif), SUM(wallet_dif), SUM(total_dif) FROM {}
                   """.format(table))
    rows = cursor.fetchone()

    print('=====================================')
    print('Total income:          ', rows[0], 'THB')
    print('-------------------------------------')
    print('Total bank spending:   ', rows[1], 'THB')
    print('Total wallet spending: ', rows[2], 'THB')
    print('-------------------------------------')
    print('Total spending:        ', rows[3], 'THB')
    print('=====================================')

    cursor.close()
    connection.close()

insert_data(table, date, income, bank, wallet)
show_sum()