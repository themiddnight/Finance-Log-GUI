try:
    from app_view import UIview
    from app_model import DataManage
except ModuleNotFoundError:
    from .app_view import UIview
    from .app_model import DataManage

class Controller:
    def __init__(self):
        self.model = DataManage()
        self.view  = UIview(self)
        self.months_name = {
            "01": "January", "02": "February", "03": "March",
            "04": "April", "05": "May", "06": "June",
            "07": "July", "08": "August", "09": "September",
            "10": "October", "11": "November", "12": "December"} 
        
    def fmt_num_out(self, value: int|float) -> str:
        '''Format int/float to string #,###'''
        if value is None:   
            output = ''
        else:               
            output = '{:,}'.format(value)
        return output
    

    def fmt_num_in(self, value: int|float) -> int|float:
        '''Format float to 2 places decimal'''
        return round(value, 2)
    

    def init_table(self):
        '''Set the latest table as current table. 
        If no table, create current date as a new one.'''
        try:        # set latest table as init table
            table_list = self.model.get_table_list()
            self.model.table = table_list[-1]
        except:     # if no table list, pass it and use default
            self.model.new_table()

    def get_theme_list(self):
        return self.model.theme_list


    def get_app_geo(self) -> str:
        '''Get the main window geometry from pref.json'''
        self.model.load_pref()
        return self.model.pref["app_geometry"]
    

    def save_app_geo(self, screen_size: str):
        '''Save the main window geometry to pref.json'''
        self.model.pref["app_geometry"] = screen_size
        self.model.save_pref()


    def get_app_theme(self):
        self.model.load_pref()
        return self.model.pref["app_theme"]
    

    def save_app_theme(self, theme: str):
        self.model.pref["app_theme"] = theme
        self.model.save_pref()


    def get_current_table(self) -> str:
        return self.model.table


    def get_table_list(self) -> tuple:
        return self.model.get_table_list()
    

    def set_current_table(self, table: str):
        self.model.table = table
    

    def get_table_data(self) -> tuple:
        '''Returns ([id, date, income, bank, cash, 
        bank_dif, cash_dif, total_dif, notes])'''
        data_raw = self.model.get_table_data()
        data = []
        for i in data_raw:
            income    = self.fmt_num_out(i[2])
            bank      = self.fmt_num_out(i[3])
            cash      = self.fmt_num_out(i[4])
            bank_dif  = self.fmt_num_out(i[5])
            cash_dif  = self.fmt_num_out(i[6])
            total_dif = self.fmt_num_out(i[7])
            if i[8] is None:
                notes = ''
            else:
                notes = '  {}'.format(i[8])
            data.append([i[0], i[1], income, bank, cash, 
                         bank_dif, cash_dif, total_dif, notes])
        return data
    

    def get_table_sum(self) -> tuple:
        '''Returns [income, bank_diff, cash_diff, total_diff]'''
        data_sum_raw = self.model.get_table_sum()
        try:
            data_sum = (
                self.fmt_num_out(self.fmt_num_in(data_sum_raw[0])),
                self.fmt_num_out(self.fmt_num_in(data_sum_raw[1])),
                self.fmt_num_out(self.fmt_num_in(data_sum_raw[2])),
                self.fmt_num_out(self.fmt_num_in(data_sum_raw[3])))
            return data_sum
        except: # if no data, return no data
            return data_sum_raw
    

    def get_rotate_table(self) -> tuple:
        '''Returns ([day], [income], [bank], [cash], 
        [bank_d], [cash_d], [sum_d], [notes]), [sum_remain]'''
        cols_data, sum_remain = self.model.get_rotate_table()
        date_ls   = [i.split('-')[-1] for i in cols_data[0]]
        income_ls = [0 if i is None else i for i in cols_data[1]]
        bank_ls   = cols_data[2]
        cash_ls   = cols_data[3]
        bank_d_ls = cols_data[4]
        cash_d_ls = cols_data[5]
        sum_d_ls  = [0 if i is None else i for i in cols_data[6]]
        notes_ls  = ['' if i is None else i for i in cols_data[7]]
        return (date_ls, income_ls, bank_ls, cash_ls, 
                bank_d_ls, cash_d_ls, sum_d_ls, notes_ls), sum_remain
    

    def submit_data(self, date: str, income:int| float, bank:int| float, 
                    cash: int| float, notes: str) -> bool:
        try:
            self.model.date = date
            if income == '':
                self.model.income = None
            else:
                self.model.income = self.fmt_num_in(float(income))
            self.model.bank  = self.fmt_num_in(float(bank))
            self.model.cash  = self.fmt_num_in(float(cash))
            self.model.notes = str(notes)
            month = self.months_name[date.split('-')[1]]
            year  = date.split('-')[0]
            self.model.table = '{} {}'.format(month, year)
            # check if current table exists in db
            table_list = self.model.get_table_list()
            if self.model.table not in table_list:
                self.model.new_table()
            self.model.insert_data()
            return True
        except ValueError:
            return False


    def delete_row(self):
        self.model.delete_row()


    def delete_table(self):
        self.model.delete_table()
        self.init_table()


    def edit_row(self, *args):
        '''id, date, notes'''
        self.model.edit_row(*args)


    def run(self):
        self.init_table()
        self.view.refresh_ui()
        self.view.mainloop()


if __name__ == "__main__":
    controller = Controller()
    controller.run()