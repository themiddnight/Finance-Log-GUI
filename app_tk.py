import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.pref_path = 'data/pref.json'
        with open(self.pref_path, 'r') as f:
            app_pref = json.load(f)

        self.title('Finance Logging')
        self.geometry(app_pref["app_geometry"])
        self.minsize(1000, 430)

        # ---------- create widget -----------

        self.input_frm  = Frame(self, padding = 10)
        self.date_l     = Label(self.input_frm, text = 'Date:')
        self.date_ent   = DateEntry(self.input_frm, date_pattern = 'yyyy-MM-dd', 
                                firstweekday = 'sunday', showweeknumbers = False, 
                                showothermonthdays = False)
        self.income_l   = Label(self.input_frm, text = 'Income:')
        self.income_ent = tk.Entry(self.input_frm, width = 15)
        self.banl_l     = Label(self.input_frm, text = 'Bank Remaining: *')
        self.bank_ent   = tk.Entry(self.input_frm, width = 15)
        self.wallet_l   = Label(self.input_frm, text = 'Wallet Remaining: *')
        self.wallet_ent = tk.Entry(self.input_frm, width = 15)
        self.notes_l    = Label(self.input_frm, text = 'Notes:')
        self.notes_ent  = tk.Entry(self.input_frm, width = 25)
        self.submit_btn = Button(self.input_frm, text = 'Submit',
                                command = self.submit_data)

        self.get_tabl_frm   = Frame(self, padding = 10)
        self.sel_tabl_l     = Label(self.get_tabl_frm, text = 'Select table:')
        self.sel_tabl_comb  = Combobox(self.get_tabl_frm, state = 'readonly')
        self.del_tabl_btn   = Button(self.get_tabl_frm, text = 'Delete This Table', 
                                     command = self.delete_table)
        self.del_row_btn    = Button(self.get_tabl_frm, text = 'Delete Latest Row', 
                                     command = self.delete_row)

        self.tab_view  = Notebook(self)
        self.table_frm = Frame(self.tab_view)
        self.graph_frm = Frame(self.tab_view)

        gen_tabl_w  = 80
        col_list    = ('', 'Date', 'Income', 
                        'Bank Remaining', 'Wallet Remaining', 
                        'Bank Spending', 'Wallet Spending', 
                        'Total  Spending', 'Notes')
        col_w_list  = (0, 70, gen_tabl_w, gen_tabl_w, gen_tabl_w, 
                        gen_tabl_w, gen_tabl_w, gen_tabl_w, 170)
        col_an_list = ('w', 'w', 'e', 'e', 'e', 'e', 'e', 'e', 'w')
        self.scrl_table  = Scrollbar(self.table_frm)

        # generate table head
        self.finance_tab    = Treeview(self.table_frm, columns = col_list[1:], 
                                    yscrollcommand = self.scrl_table.set)
        for i in range(len(col_list)):
            self.finance_tab.column(f'#{i}', width = col_w_list[i], 
                                anchor = col_an_list[i])
            self.finance_tab.heading(f'#{i}', text = col_list[i])

        # generate graph canvas
        self.figure         = Figure(figsize = (6, 2), facecolor = "#222222")
        self.graph_canvas   = FigureCanvasTkAgg(self.figure, master = self.graph_frm)
        self.graph_canvas.get_tk_widget().configure(background = 'black')


        # ---------- place widget ----------

        self.get_tabl_frm.pack   (fill = 'both', pady=(10,0), padx=10)
        self.sel_tabl_l.pack     (side = 'left')
        self.sel_tabl_comb.pack  (side = 'left')
        self.del_tabl_btn.pack   (side = 'right')
        self.del_row_btn.pack    (side = 'right', padx = 10)

        self.tab_view.add(self.table_frm, text = 'Table')
        self.tab_view.add(self.graph_frm, text = 'Graph')
        self.tab_view.pack(fill = 'both', expand = 1)

        self.scrl_table.pack(side = 'right', fill = 'y')
        self.finance_tab.pack (fill = 'both', expand = 1, padx = 10, pady = (0,10))

        self.graph_canvas.get_tk_widget().pack(expand=1, fill='both')

        self.input_frm.pack  (pady=(0,10))
        self.date_l.grid     (sticky = 'w', row = 0, column = 0, padx = 5)
        self.date_ent.grid   (row = 1, column = 0, padx = 5)
        self.income_l.grid   (sticky = 'w', row = 0, column = 1, padx = 5)
        self.income_ent.grid (row = 1, column = 1, padx = 5)
        self.banl_l.grid     (sticky = 'w', row = 0, column = 2, padx = 5)
        self.bank_ent.grid   (row = 1, column = 2, padx = 5)
        self.wallet_l.grid   (sticky = 'w', row = 0, column = 3, padx = 5)
        self.wallet_ent.grid (row = 1, column = 3, padx = 5)
        self.notes_l.grid    (sticky = 'w', row = 0, column = 4, padx = 5)
        self.notes_ent.grid  (row = 1, column = 4, padx = 5)
        self.submit_btn.grid (row = 1, column = 5, padx = 5)


        # ---------- validate / get events ----------

        self.bind('<Configure>', self.screen_resize_event)
        self.income_ent.bind('<Return>', self.submit_data)
        self.bank_ent.bind('<Return>', self.submit_data)
        self.wallet_ent.bind('<Return>', self.submit_data)
        self.notes_ent.bind('<Return>', self.submit_data)
        self.sel_tabl_comb.bind("<<ComboboxSelected>>", self.select_table)

    ###############################################
        

    def screen_resize_event(self, *args):
        with open(self.pref_path, 'w') as f:
            json.dump({"app_geometry": self.geometry()}, f)


    def init_ui(self):
        current_table = datetime.now().strftime('%B %Y')
        main.init(current_table)
        table_list = main.get_tablelist()
        self.sel_tabl_comb['values'] = table_list
        self.sel_tabl_comb.current(table_list.index(current_table))
        self.generate_table(current_table)
        self.generate_graph(current_table)


    def submit_data(self, *args):
        latest_entry = self.focus_get()
        try:
            date  = self.date_ent.get_date().strftime("%Y-%m-%d")
            table = '{} {}'.format(main.get_month_name(date.split('-')[1]),
                                    date.split('-')[0])
            if self.income_ent.get() == '': 
                income = None
            else: 
                income = float(self.income_ent.get())
            bank   = float(self.bank_ent.get())
            wallet = float(self.wallet_ent.get())
            if self.notes_ent.get() == '': 
                notes = None
            else: 
                notes = self.notes_ent.get()
            main.insert_data(table, date, income, bank, wallet, notes)
            # rebuild ui
            self.generate_table(table)
            self.generate_graph(table)
            table_list = main.get_tablelist()
            self.sel_tabl_comb['values'] = table_list
            self.sel_tabl_comb.current(table_list.index(table))
            self.income_ent.delete(0, 'end')
            self.bank_ent.delete(0, 'end')
            self.wallet_ent.delete(0, 'end')
            self.notes_ent.delete(0, 'end')
        except ValueError:
            messagebox.showwarning(message = 'The input is not valid.')
        self.focus()
        latest_entry.focus()
            

    def select_table(self, *args):
        table = self.sel_tabl_comb.get()
        self.generate_table(table)
        self.generate_graph(table)


    def delete_row(self):
        table = self.sel_tabl_comb.get()
        confirm = messagebox.askquestion(
            message = 'Delete the latest row?')
        if confirm == 'yes':
            main.delete_row(table)
            self.generate_table(table)
            self.generate_graph(table)


    def delete_table(self):
        table = self.sel_tabl_comb.get()
        confirm = messagebox.askquestion(
            message = 'Are you sure to delete this table?')
        if confirm == 'yes':
            main.delete_table(table)
            self.init_ui()


    def generate_table(self, table):
        self.finance_tab.delete(*self.finance_tab.get_children())
        all_data    = main.get_tabledata(table)
        data        = all_data[0]
        data_sum    = all_data[1]
        def format_value(value):
            if value is None:   output = ''
            else:               output = '{:,}'.format(value)
            return output
        for i in data:
            income      = format_value(i[2])
            bank        = format_value(i[3])
            wallet      = format_value(i[4])
            bank_dif    = format_value(i[5])
            wallet_dif  = format_value(i[6])
            total_dif   = format_value(i[7])
            if i[8] is None:    notes       = ''
            else:               notes       = '  {}'.format(i[8])
            self.finance_tab.insert(parent='', index = 'end', 
                                values = (i[1], income, bank, wallet, 
                                bank_dif, wallet_dif, total_dif, notes))
            
        self.finance_tab.insert(parent = '', index = 'end', 
                        values = ('--------------', '--------------',
                                    '--------------', '--------------',
                                    '--------------', '--------------',
                                    '--------------',
                                    '-------------------------------',))
        income_sum      = format_value(data_sum[0])
        bank_dif_sum    = format_value(data_sum[1])
        wallet_dif_sum  = format_value(data_sum[2])
        total_dif_sum   = format_value(data_sum[3])
        self.finance_tab.insert(parent = '', index = 'end', 
                            values = ('Grand Total', income_sum, '', '', 
                                        bank_dif_sum, wallet_dif_sum, 
                                        total_dif_sum, ''))


    def generate_graph(self, table):
        if main.get_rotate_table(table):
            (day_list, income_list, bank_list, wallet_list, bank_d_list, 
             wallet_d_list, sum_remain, note_list) = main.get_rotate_table(table)
            
            self.figure.clear()
            
            ax = self.figure.add_subplot(211, facecolor='#131313')
            ax.plot(day_list, bank_d_list, label = "Bank")
            ax.plot(day_list, wallet_d_list, label = "Wallet")
            ax.grid(linestyle = '--', linewidth = 0.1)
            ax.legend()
            ax.invert_yaxis()
            ax.tick_params(axis="both", colors = "white", labelsize = 8)
            ax.legend(fontsize = 9, facecolor = "lightgray")

            ax = self.figure.add_subplot(212, facecolor = '#131313')
            ax.bar(day_list, income_list, label = "Income")
            ax.plot(day_list, sum_remain, label = "Remaining")
            ax.grid(linestyle = '--', linewidth = 0.1)
            ax.legend()
            ax.tick_params(axis="both", colors = "white", labelsize = 8)
            ax.legend(fontsize = 9, facecolor = "lightgray")
            self.figure.subplots_adjust(left = 0.07, bottom = 0.08,
                                    right = 0.95, top = 0.94)
            num = 0
            for i in day_list:
                day = int(i)
                ax.annotate(note_list[num], xy = (num, 0), xytext = (-5,10), 
                            textcoords = 'offset points', rotation = 90, 
                            fontsize = 10, fontname = 'Tahoma', color = '#cccccc')
                num += 1

        self.graph_canvas.draw()


if __name__ == "__main__":
    app = Root()
    app.init_ui()
    app.mainloop()