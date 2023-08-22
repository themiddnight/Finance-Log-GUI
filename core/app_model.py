import sqlite3
import json
import os
from datetime import datetime

class DataManage:
    def __init__(self):
        data_dir = os.path.expanduser('~') + '/Documents/Finance Logging/'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        with open('data/themes.json', 'r') as f:
            self.theme_list = json.load(f)
            
        self.pref_path = data_dir + 'pref.json'
        self.db_file   = data_dir + 'database.db'
        self.table  = datetime.now().strftime('%B %Y')
        self.id     = 0
        self.date   = ''
        self.income = 0
        self.bank   = 0
        self.cash   = 0
        self.bank_dif  = 0
        self.cash_dif  = 0
        self.total_dif = 0
        self.notes  = ''
        self.pref = {"app_geometry":"1124x600+350+200", 
                     "app_theme":"bright"}
        self.columns = ['date', 'income', 'bank', 'cash', 
                        'bank_dif', 'cash_dif', 'total_dif', 'notes']
        self.connection = sqlite3.connect(self.db_file)
        

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
        cursor = self.connection.cursor()
        cursor.execute(f"""--sql
                    CREATE TABLE '{self.table}' 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    date TEXT, income NUMERIC, bank NUMERIC, 
                    cash NUMERIC, bank_dif NUMERIC, cash_dif NUMERIC, 
                    total_dif NUMERIC, notes TEXT);""")
        cursor.close()


    def get_table_list(self) -> list | None:
        cursor = self.connection.cursor()
        # get all tables
        cursor.execute("""--sql
                        SELECT name FROM sqlite_master 
                        WHERE type = 'table';
                        """)
        data = cursor.fetchall()
        cursor.close()
        return data


    def get_table_data(self) -> list | None:
        '''Returns ([id, date, income, bank, cash, 
        bank_dif, cash_dif, total_dif, notes])'''
        cursor = self.connection.cursor()
        # get entire table
        cursor.execute(f"""--sql
                        SELECT * FROM '{self.table}';
                        """)
        data = cursor.fetchall()
        cursor.close()
        return data


    def get_table_sum(self) -> list | None:
        '''Returns [income, bank_diff, cash_diff, total_diff]'''
        cursor = self.connection.cursor()
        # get sum
        cursor.execute(f"""--sql
                    SELECT SUM(income), SUM(bank_dif), SUM(cash_dif), 
                    SUM(total_dif) FROM '{self.table}';""")
        sum = cursor.fetchone()
        cursor.close()
        return sum


    def get_rotate_table(self) -> tuple[list, list]:
        '''Returns ([date], [income], [bank], [cash], 
        [bank_d], [cash_d], [sum_d], [notes]), [sum_remain]'''
        cursor = self.connection.cursor()
        column_datas = []
        for col in self.columns:
            cursor.execute(f"""SELECT {col} FROM '{self.table}'""")
            data = cursor.fetchall()
            column_datas.append([i[0] for i in data])
        cursor.close()
        sum_remain = [x + y for x, y in zip(column_datas[2], column_datas[3])]
        return column_datas, sum_remain


    def insert_data(self):
        cursor = self.connection.cursor()
        cursor.execute("""--sql
                    INSERT INTO '{}' (date, income, bank, cash, 
                    bank_dif, cash_dif, total_dif, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);""".format(self.table),
                    (self.date, self.income, self.bank, self.cash,
                    self.bank_dif, self.cash_dif, self.total_dif, self.notes))
        self.connection.commit()
        cursor.close()


    def delete_row(self):
        cursor = self.connection.cursor()
        # read latest row
        try:
            cursor.execute(f"""--sql
                        SELECT ID FROM '{self.table}'
                        ORDER by ID DESC;""")
            id = cursor.fetchone()[0]
            cursor.execute(f"""--sql
                        DELETE from '{self.table}' WHERE rowid = {id}""")
            self.connection.commit()
        except:
            pass
        cursor.close()


    def delete_table(self):
        cursor = self.connection.cursor()
        # read latest row
        try:
            cursor.execute(f"""--sql
                        DROP TABLE '{self.table}';""")
            self.connection.commit()
        except:
            pass
        cursor.close()


    def edit_row(self):
        cursor = self.connection.cursor()
        cursor.execute(f"""--sql
                       UPDATE "{self.table}" SET date = "{self.date}", 
                       notes = "{self.notes}" WHERE ID = {self.id};""")
        self.connection.commit()
        cursor.close()