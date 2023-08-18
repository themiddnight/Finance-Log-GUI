import sqlite3
import json
from datetime import datetime

class DataManage:
    def __init__(self):
        self.pref_file : str = "core/data/pref.json"
        self.db_file   : str = 'core/data/database.db'
        self.win_geo   : str = "1003x600+350+300"
        self.table  : str = datetime.now().strftime('%B %Y')
        self.date   : str = ''
        self.income : int|float = 0
        self.bank   : int|float = 0
        self.cash   : int|float = 0
        self.notes  : str = ''
        self.connection = sqlite3.connect(self.db_file)
        

    def load_pref(self) -> dict:
        try:
            with open(self.pref_file, 'r') as f:
                pref = json.load(f)
            return pref
        except FileNotFoundError:
            with open(self.pref_file, 'w') as f:
                json.dump({"app_geometry": self.win_geo}, f)
            with open(self.pref_file, 'r') as f:
                pref = json.load(f)
            return pref
    
    
    def save_pref(self, data: str, value: str):
        with open(self.pref_file, 'w') as f:
            json.dump({data: value}, f)


    def set_table_name(self):
        month = self.date.split('-')[1]
        year = self.date.split('-')[2]
        self.table = '{} {}'.format(month, year)
    

    def new_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("""--sql
                    CREATE TABLE '{}' 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, 
                    cash NUMERIC, bank_dif NUMERIC, cash_dif NUMERIC, 
                    total_dif NUMERIC, notes TEXT);""".format(self.table))
        cursor.close()
        connection.close()


    def get_table_list(self) -> tuple|None:
        connection = sqlite3.connect(self.db_file)
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
            tables_list = [i[0] for i in data]
            def get_month_year(date_str):   # sorting table name
                months = {'January': 1, 'February': 2, 'March': 3, 
                        'April': 4, 'May': 5, 'June': 6, 'July': 7, 
                        'August': 8, 'September': 9, 'October': 10, 
                        'November': 11, 'December': 12}
                month, year = date_str.split(' ')
                return (year, months[month])
            # Sort the list using the custom sorting key
            sorted_table_list = sorted(tables_list, key = get_month_year)
        else:
            # tables_list = None
            sorted_table_list = None
        return sorted_table_list


    def get_table_data(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # get entire table
        cursor.execute("""--sql
                        SELECT * FROM '{}';
                        """.format(self.table))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data


    def get_table_sum(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # get sum
        cursor.execute("""--sql
                    SELECT SUM(income), SUM(bank_dif), SUM(cash_dif), 
                    SUM(total_dif) FROM '{}';""".format(self.table))
        sum = cursor.fetchone()
        cursor.close()
        connection.close()
        return sum


    def get_rotate_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("""PRAGMA table_info("{}")""".format(self.table))
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]
        columns.pop(0)
        column_datas = []
        for col in columns:
            cursor.execute("""SELECT {} FROM '{}'""".format(col, self.table))
            data = cursor.fetchall()
            column_datas.append([i[0] for i in data])
        cursor.close()
        connection.close()
        sum_remain = [x + y for x, y in zip(column_datas[2], column_datas[3])]
        return column_datas, sum_remain
        # day_list, income_list, bank_list, cash_list, bank_d_list, cash_d_list, sum_remain


    def insert_data(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # self.init(self.table)
        # read 2 latest row
        cursor.execute("""--sql
                    SELECT ID, bank, cash FROM '{}'
                    ORDER by ID DESC;
                    """.format(self.table))
        rows = cursor.fetchmany(2)
        # check latest id
        if not rows:        # if empty, start with 0
            id = 0         
        else:               # if has data, increase id
            id = rows[0][0] + 1   
        # calculate difference
        if len(rows) >= 1:  # if it has a row prior to find difference
            if not self.income:
                bank_dif = round((self.bank - rows[0][1]), 2)
            else:
                bank_dif = round(((self.bank - rows[0][1]) - self.income), 2)
            cash_dif = round((self.cash - rows[0][2]), 2)
            total_dif = round((bank_dif + cash_dif), 2)
        else:
            if not self.income:
                bank_dif = None
                total_dif = None
            else:
                bank_dif = round((self.bank - self.income), 2)
                total_dif = bank_dif
            cash_dif = None
        # add item to table
        cursor.execute("""--sql
                    INSERT INTO '{}' (ID, date, income, bank, cash, 
                    bank_dif, cash_dif, total_dif, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""".format(self.table),
                    (id, self.date, self.income, self.bank, self.cash,
                    bank_dif, cash_dif, total_dif, self.notes))
        connection.commit()
        cursor.close()
        connection.close()


    def delete_row(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # read latest row
        try:
            cursor.execute("""--sql
                        SELECT ID FROM '{}'
                        ORDER by ID DESC;
                        """.format(self.table))
            id = cursor.fetchone()[0]
            cursor.execute("""--sql
                        DELETE from '{}' WHERE rowid = {}
                        """.format(self.table, id))
            connection.commit()
        except:
            pass
        cursor.close()
        connection.close()


    def delete_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # read latest row
        try:
            cursor.execute("""--sql
                        DROP TABLE '{}';
                        """.format(self.table))
            connection.commit()
        except:
            pass
        cursor.close()
        connection.close()


    def edit_row(self, id, date, notes):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("""--sql
                       UPDATE "{}" SET date = "{}", notes = "{}" WHERE ID = {};
                       """.format(self.table, date, notes, id))
        connection.commit()
        cursor.close()
        connection.close()