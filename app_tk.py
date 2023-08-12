import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import main

with open('data/pref.json', 'r') as f:
    app_pref = json.load(f)

app = tk.Tk()
app.title('Finance Logging')
app.geometry(app_pref["app_geometry"])
app.minsize(1000, 430)


def init_ui():
    current_table = datetime.now().strftime('%B %Y')
    main.init(current_table)
    table_list = main.get_tablelist()
    sel_tabl_comb['values'] = table_list
    sel_tabl_comb.current(table_list.index(current_table))
    generate_table(current_table)
    generate_graph(current_table)


def submit_data(*args):
    latest_entry = app.focus_get()
    try:
        date  = date_ent.get_date().strftime("%Y-%m-%d")
        table = '{} {}'.format(main.get_month_name(date.split('-')[1]),
                                date.split('-')[0])
        if income_ent.get() == '': 
            income = None
        else: 
            income = float(income_ent.get())
        bank   = float(bank_ent.get())
        wallet = float(wallet_ent.get())
        if notes_ent.get() == '': 
            notes = None
        else: 
            notes = notes_ent.get()
        main.insert_data(table, date, income, bank, wallet, notes)
        # rebuild ui
        generate_table(table)
        generate_graph(table)
        table_list = main.get_tablelist()
        sel_tabl_comb['values'] = table_list
        sel_tabl_comb.current(table_list.index(table))
        income_ent.delete(0, 'end')
        bank_ent.delete(0, 'end')
        wallet_ent.delete(0, 'end')
        notes_ent.delete(0, 'end')
    except ValueError:
        messagebox.showwarning(message = 'The input is not valid.')
    app.focus()
    latest_entry.focus()
        

def select_table(*args):
    table = sel_tabl_comb.get()
    generate_table(table)
    generate_graph(table)


def delete_row():
    table = sel_tabl_comb.get()
    confirm = messagebox.askquestion(
        message = 'Delete the latest row?')
    if confirm == 'yes':
        main.delete_row(table)
        generate_table(table)
        generate_graph(table)


def delete_table():
    table = sel_tabl_comb.get()
    confirm = messagebox.askquestion(
        message = 'Are you sure to delete this table?')
    if confirm == 'yes':
        main.delete_table(table)
        init_ui()


def generate_table(table):
    finance_tab.delete(*finance_tab.get_children())
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
        finance_tab.insert(parent='', index = 'end', 
                            values = (i[1], income, bank, wallet, 
                            bank_dif, wallet_dif, total_dif, notes))
        
    finance_tab.insert(parent = '', index = 'end', 
                    values = ('--------------', '--------------',
                                '--------------', '--------------',
                                '--------------', '--------------',
                                '--------------',
                                '-------------------------------',))
    income_sum      = format_value(data_sum[0])
    bank_dif_sum    = format_value(data_sum[1])
    wallet_dif_sum  = format_value(data_sum[2])
    total_dif_sum   = format_value(data_sum[3])
    finance_tab.insert(parent = '', index = 'end', 
                        values = ('Grand Total', income_sum, '', '', 
                                    bank_dif_sum, wallet_dif_sum, 
                                    total_dif_sum, ''))


def generate_graph(table):
    # get data
    data, _ = main.get_tabledata(table)
    arr = np.array(data)
    # dataset
    day_list = [i.split('-')[-1] for i in arr[:,1]]
    income_list = [i if i is not None else 0 for i in arr[:,2]]
    bank_list = arr[:,3]
    wallet_list = arr[:,4]
    bank_d_list = arr[:,5]
    wallet_d_list = arr[:,6]
    sum_remain = np.sum([bank_list, wallet_list], axis = 0)
    
    figure.clear()
    
    ax = figure.add_subplot(211, facecolor='#181818')
    ax.plot(day_list, bank_d_list, label = "Bank")
    ax.plot(day_list, wallet_d_list, label = "Wallet")
    ax.grid(linestyle = '--', linewidth = 0.3)
    ax.legend()
    ax.invert_yaxis()
    ax.tick_params(axis="both", colors = "white", labelsize = 8)
    ax.legend(fontsize = 8, facecolor = "lightgray")

    ax = figure.add_subplot(212, facecolor = '#181818')
    ax.bar(day_list, income_list, label = "Income")
    ax.plot(day_list, sum_remain, label = "Remaining")
    ax.grid(linestyle = '--', linewidth = 0.3)
    ax.legend()
    ax.tick_params(axis="both", colors = "white", labelsize = 8)
    ax.legend(fontsize = 8, facecolor = "lightgray")
    figure.subplots_adjust(left = 0.07, bottom = 0.08,
                            right = 0.95, top = 0.94)
    graph_canvas.draw()
    

def screen_resize_event(*args):
    with open('data/pref.json', 'w') as f:
        json.dump({"app_geometry": app.geometry()}, f)


# ---------- create widget -----------

input_frm   = Frame(app, padding = 10)
date_l      = Label(input_frm, text = 'Date:')
date_ent    = DateEntry(input_frm, date_pattern = 'yyyy-MM-dd', 
                        firstweekday = 'sunday', showweeknumbers = False, 
                        showothermonthdays = False)
income_l    = Label(input_frm, text = 'Income:')
income_ent  = tk.Entry(input_frm, width = 15)
banl_l      = Label(input_frm, text = 'Bank Remaining: *')
bank_ent    = tk.Entry(input_frm, width = 15)
wallet_l    = Label(input_frm, text = 'Wallet Remaining: *')
wallet_ent  = tk.Entry(input_frm, width = 15)
notes_l     = Label(input_frm, text = 'Notes:')
notes_ent   = tk.Entry(input_frm, width = 25)
submit_btn  = Button(input_frm, text = 'Submit', width = 7, 
                     command = submit_data)

sep1 = Separator(app, orient = 'horizontal')

get_tabl_frm    = Frame(app, padding = 10)
sel_tabl_l      = Label(get_tabl_frm, text = 'Select table:')
sel_tabl_comb   = Combobox(get_tabl_frm, state = 'readonly')
del_tabl_btn    = Button(get_tabl_frm, text = 'Delete This Table', 
                         command = delete_table)
del_row_btn     = Button(get_tabl_frm, text = 'Delete Latest Row', 
                         command = delete_row)

tab_view  = Notebook(app)
table_frm = Frame(tab_view)
graph_frm = Frame(tab_view)

gen_tabl_w = 80
col_list    = ('', 'Date', 'Income', 
                'Bank Remaining', 'Wallet Remaining', 
                'Bank Spending', 'Wallet Spending', 
                'Total  Spending', 'Notes')
col_w_list  = (0, 70, gen_tabl_w, gen_tabl_w, gen_tabl_w, 
                gen_tabl_w, gen_tabl_w, gen_tabl_w, 200)
col_an_list = ('w', 'w', 'e', 'e', 'e', 'e', 'e', 'e', 'w')
scrl_table = Scrollbar(table_frm)

# generate table head
finance_tab = Treeview(table_frm, columns = col_list[1:], 
                       yscrollcommand = scrl_table.set)
for i in range(len(col_list)):
    finance_tab.column(f'#{i}', width = col_w_list[i], 
                        anchor = col_an_list[i])
    finance_tab.heading(f'#{i}', text = col_list[i])

# generate graph canvas
figure = Figure(figsize=(6, 2), facecolor = "#222222")
graph_canvas = FigureCanvasTkAgg(figure, master=graph_frm)
graph_canvas.get_tk_widget().configure(background='black')


# ---------- place widget ----------

get_tabl_frm.pack   (fill = 'both', pady=(10,0), padx=10)
sel_tabl_l.pack     (side = 'left')
sel_tabl_comb.pack  (side = 'left')
del_tabl_btn.pack   (side = 'right')
del_row_btn.pack    (side = 'right', padx = 10)

tab_view.add(table_frm, text = 'Table')
tab_view.add(graph_frm, text = 'Graph')
tab_view.pack(fill = 'both', expand = 1)

scrl_table.pack(side = 'right', fill = 'y')
finance_tab.pack (fill = 'both', expand = 1, padx = 10, pady = (0,10))

graph_canvas.get_tk_widget().pack(expand=1, fill='both')

input_frm.pack  (pady=(0,10))
date_l.grid     (sticky = 'w', row = 0, column = 0, padx = 5)
date_ent.grid   (row = 1, column = 0, padx = 5)
income_l.grid   (sticky = 'w', row = 0, column = 1, padx = 5)
income_ent.grid (row = 1, column = 1, padx = 5)
banl_l.grid     (sticky = 'w', row = 0, column = 2, padx = 5)
bank_ent.grid   (row = 1, column = 2, padx = 5)
wallet_l.grid   (sticky = 'w', row = 0, column = 3, padx = 5)
wallet_ent.grid (row = 1, column = 3, padx = 5)
notes_l.grid    (sticky = 'w', row = 0, column = 4, padx = 5)
notes_ent.grid  (row = 1, column = 4, padx = 5)
submit_btn.grid (row = 1, column = 5, padx = 5)


# ---------- validate / get events ----------

app.bind('<Configure>', screen_resize_event)
income_ent.bind('<Return>', submit_data)
bank_ent.bind('<Return>', submit_data)
wallet_ent.bind('<Return>', submit_data)
notes_ent.bind('<Return>', submit_data)
sel_tabl_comb.bind("<<ComboboxSelected>>", select_table)


init_ui()
app.mainloop()