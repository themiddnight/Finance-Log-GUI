import sqlite3
import json
import os
from datetime import datetime

class DataManage:
    def __init__(self):
        with open('core/themes.json', 'r') as f:
            self.theme_list = json.load(f)

        data_dir = os.path.expanduser('~') + '/Documents/Finance Logging/'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.pref_path = data_dir + 'pref.json'
        self.db_file   = data_dir + 'database.db'
        self.table  = datetime.now().strftime('%B %Y')
        self.date   = ''
        self.income = 0
        self.bank   = 0
        self.cash   = 0
        self.notes  = ''
        self.pref = {"app_geometry":"1124x600+350+200", 
                     "app_theme":"bright"}
        self.columns = ['date', 'income', 'bank', 'cash', 
                        'bank_dif', 'cash_dif', 'total_dif', 'notes']
        

    def load_pref(self):
        try:
            with open(self.pref_path, 'r') as f:
                self.pref = json.load(f)
        except:
            with open(self.pref_path, 'w') as f:
                json.dump(self.pref, f)
            with open(self.pref_path, 'r') as f:
                self.pref = json.load(f)
    
    
    def save_pref(self):
        with open(self.pref_path, 'w') as f:
            json.dump(self.pref, f)
    

    def new_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(f"""--sql
                    CREATE TABLE '{self.table}' 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, 
                    cash NUMERIC, bank_dif NUMERIC, cash_dif NUMERIC, 
                    total_dif NUMERIC, notes TEXT);""")
        cursor.close()
        connection.close()


    def get_table_list(self) -> list | None:
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
        return data


    def get_table_data(self) -> list | None:
        '''Returns ([id, date, income, bank, cash, 
        bank_dif, cash_dif, total_dif, notes])'''
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # get entire table
        cursor.execute(f"""--sql
                        SELECT * FROM '{self.table}';
                        """)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data


    def get_table_sum(self) -> list | None:
        '''Returns [income, bank_diff, cash_diff, total_diff]'''
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # get sum
        cursor.execute(f"""--sql
                    SELECT SUM(income), SUM(bank_dif), SUM(cash_dif), 
                    SUM(total_dif) FROM '{self.table}';""")
        sum = cursor.fetchone()
        cursor.close()
        connection.close()
        return sum


    def get_rotate_table(self) -> tuple[list, list]:
        '''Returns ([date], [income], [bank], [cash], 
        [bank_d], [cash_d], [sum_d], [notes]), [sum_remain]'''
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        column_datas = []
        for col in self.columns:
            cursor.execute(f"""SELECT {col} FROM '{self.table}'""")
            data = cursor.fetchall()
            column_datas.append([i[0] for i in data])
        cursor.close()
        connection.close()
        sum_remain = [x + y for x, y in zip(column_datas[2], column_datas[3])]
        return column_datas, sum_remain


    def insert_data(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # read 2 latest row
        cursor.execute(f"""--sql
                    SELECT ID, bank, cash FROM '{self.table}'
                    ORDER by ID DESC;""")
        rows = cursor.fetchmany(2) 
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
                    INSERT INTO '{}' (date, income, bank, cash, 
                    bank_dif, cash_dif, total_dif, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);""".format(self.table),
                    (self.date, self.income, self.bank, self.cash,
                    bank_dif, cash_dif, total_dif, self.notes))
        connection.commit()
        cursor.close()
        connection.close()


    def delete_row(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # read latest row
        try:
            cursor.execute(f"""--sql
                        SELECT ID FROM '{self.table}'
                        ORDER by ID DESC;""")
            id = cursor.fetchone()[0]
            cursor.execute(f"""--sql
                        DELETE from '{self.table}' WHERE rowid = {id}""")
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
            cursor.execute(f"""--sql
                        DROP TABLE '{self.table}';""")
            connection.commit()
        except:
            pass
        cursor.close()
        connection.close()


    def edit_row(self, id: int, date: str, notes: str):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(f"""--sql
                       UPDATE "{self.table}" SET date = "{date}", 
                       notes = "{notes}" WHERE ID = {id};""")
        connection.commit()
        cursor.close()
        connection.close()