import sqlite3
import json

# get database path from json file
with open('data/path.json', 'r') as f:
    connection_path = json.load(f)['0']

def init(table):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    tables = get_tablelist()
    # check if it has tables, or current table exists
    if not tables or table not in tables:
        cursor.execute("""--sql
                    CREATE TABLE '{}' 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, wallet NUMERIC, 
                    bank_dif NUMERIC, wallet_dif NUMERIC, total_dif NUMERIC, notes TEXT);
                    """.format(table))
    cursor.close()
    connection.close()

def get_tablelist():
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    # get all tables
    cursor.execute("""--sql
                   SELECT name FROM sqlite_master 
                   WHERE type='table';
                   """)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    if data:
        data.remove(('sqlite_sequence',))
        tables = [i[0] for i in data]
    else:
        tables = None
    # sorting table name
    def get_month_year(date_str):
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 
                  'May': 5, 'June': 6, 'July': 7, 'August': 8, 
                  'September': 9, 'October': 10, 'November': 11, 'December': 12}
        month, year = date_str.split(' ')
        return (year, months[month])
    # Sort the list using the custom sorting key
    sorted_tables = sorted(tables, key = get_month_year)
    return sorted_tables


def get_tabledata(table):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    # get entire table
    cursor.execute("""--sql
                   SELECT * FROM '{}';
                   """.format(table))
    data = cursor.fetchall()
    sum_remain = data[-1][3] + data[-1][4]
    # get sum
    cursor.execute("""--sql
                   SELECT SUM(income), SUM(bank_dif), SUM(wallet_dif), SUM(total_dif) FROM '{}';
                   """.format(table))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    # table data, sum
    return data, [sum[0], sum[1], sum[2], sum[3], sum_remain]

def insert_data(table, date, income, bank, wallet, notes):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    # read 2 latest row
    cursor.execute("""--sql
                SELECT ID, bank, wallet FROM '{}'
                ORDER by ID DESC;
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
                   INSERT INTO '{}' (ID, date, income, bank, wallet, bank_dif, wallet_dif, total_dif, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                   """.format(table), (id, date, income, bank, wallet, bank_dif, wallet_dif, total_dif, notes))
    connection.commit()
    cursor.close()
    connection.close()

def delete_row(table):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    # read latest row
    try:
        cursor.execute("""--sql
                    SELECT ID FROM '{}'
                    ORDER by ID DESC;
                    """.format(table))
        id = cursor.fetchone()[0]
        cursor.execute("""--sql
                    DELETE from '{}' WHERE rowid = {}
                    """.format(table, id))
        connection.commit()
    except:
        pass
    cursor.close()
    connection.close()

def delete_table(table):
    connection = sqlite3.connect(connection_path)
    cursor = connection.cursor()
    # read latest row
    try:
        cursor.execute("""--sql
                    DROP TABLE '{}';
                    """.format(table))
        connection.commit()
    except:
        pass
    cursor.close()
    connection.close()