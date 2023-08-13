import sqlite3
import os
import numpy as np

# create/get database path from /User/Documents/ path
home_dir = os.path.expanduser('~')
db_path = home_dir + '/Documents/finance_database.db'

def get_month_name(num):
    months_name = {"01": "January", "02": "February", "03": "March",
                "04": "April", "05": "May", "06": "June",
                "07": "July", "08": "August", "09": "September",
                "10": "October", "11": "November", "12": "December"}
    return months_name[num]

def init(table):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    tables = get_tablelist()
    # check if it has tables, or current table exists
    if not tables or table not in tables:
        cursor.execute("""--sql
                    CREATE TABLE '{}' 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, 
                    wallet NUMERIC, bank_dif NUMERIC, wallet_dif NUMERIC, 
                    total_dif NUMERIC, notes TEXT);""".format(table))
        print('created ' + table)
    cursor.close()
    connection.close()


def get_tablelist():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # get all tables
    cursor.execute("""--sql
                    SELECT name FROM sqlite_master 
                    WHERE type = 'table';
                    """)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    if data:
        data.remove(('sqlite_sequence',))
        tables = [i[0] for i in data]

        def get_month_year(date_str):   # sorting table name
            months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                    'May': 5, 'June': 6, 'July': 7, 'August': 8,
                    'September': 9, 'October': 10, 'November': 11,
                    'December': 12}
            month, year = date_str.split(' ')
            return (year, months[month])
        # Sort the list using the custom sorting key
        sorted_tables = sorted(tables, key=get_month_year)
    else:
        tables = None
        sorted_tables = None
    return sorted_tables


def get_tabledata(table):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # get entire table
    cursor.execute("""--sql
                    SELECT * FROM '{}';
                    """.format(table))
    data = cursor.fetchall()
    if data:
        sum_remain = data[-1][3] + data[-1][4]
        # get sum
        cursor.execute("""--sql
                    SELECT SUM(income), SUM(bank_dif), SUM(wallet_dif), 
                    SUM(total_dif) FROM '{}';""".format(table))
        sum = cursor.fetchone()
    else:
        sum = [None, None, None, None]
        sum_remain = None
    cursor.close()
    connection.close()
    # table data, sum
    return data, [sum[0], sum[1], sum[2], sum[3], sum_remain]


def get_rotate_table(table):
    # get data
    data, _ = get_tabledata(table)
    if data:
        arr = np.array(data)
        # dataset
        day_list = [i.split('-')[-1] for i in arr[:,1]]
        income_list = [i if i is not None else 0 for i in arr[:,2]]
        bank_list = arr[:,3]
        wallet_list = arr[:,4]
        bank_d_list = arr[:,5]
        wallet_d_list = arr[:,6]
        sum_remain = np.sum([bank_list, wallet_list], axis = 0)
        note_list = []
        for i in data:
            note_list.append(i[8])
        return (day_list, income_list, bank_list, wallet_list, 
                bank_d_list, wallet_d_list, sum_remain, note_list)
    return False

def insert_data(table, date, income, bank, wallet, notes):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    init(table)
    # read 2 latest row
    cursor.execute("""--sql
                SELECT ID, bank, wallet FROM '{}'
                ORDER by ID DESC;
                """.format(table))
    rows = cursor.fetchmany(2)
    # check latest id
    if not rows:        # if empty, start with 0
        id = 0         
    else:               # if has data, increase id
        id = rows[0][0] + 1   
    # calculate difference
    if len(rows) >= 1:  # if it has a row prior to find difference
        if not income:
            bank_dif = (bank - rows[0][1])
        else:
            bank_dif = (bank - rows[0][1]) - income
        wallet_dif = wallet - rows[0][2]
        total_dif = bank_dif + wallet_dif
    else:
        if not income:
            bank_dif = None
            total_dif = None
        else:
            bank_dif = bank - income
            total_dif = bank_dif
        wallet_dif = None
    # add item to table
    cursor.execute("""--sql
                    INSERT INTO '{}' (ID, date, income, bank, wallet, 
                    bank_dif, wallet_dif, total_dif, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""".format(table),
                   (id, date, income, bank, wallet,
                    bank_dif, wallet_dif, total_dif, notes))
    connection.commit()
    cursor.close()
    connection.close()


def delete_row(table):
    connection = sqlite3.connect(db_path)
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
    connection = sqlite3.connect(db_path)
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
