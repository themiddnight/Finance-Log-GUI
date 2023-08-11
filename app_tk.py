from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import main

app = Tk()
app.title('Finance Logging')
app.geometry('1000x760+300+100')
photo = PhotoImage(file = "static/image/icon.png")
app.iconphoto(False, photo)

def init_ui():
    current_table = datetime.now().strftime('%B %Y')
    main.init(current_table)
    table_list = main.get_tablelist()
    sel_tab_comb['values'] = table_list
    sel_tab_comb.current(table_list.index(current_table))
    generate_table(current_table)


def submit_data():
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
        table_list = main.get_tablelist()
        sel_tab_comb['values'] = table_list
        sel_tab_comb.current(table_list.index(table))
        income_ent.delete(0, END)
        bank_ent.delete(0, END)
        wallet_ent.delete(0, END)
        notes_ent.delete(0, END)
    except ValueError:
        messagebox.showwarning(message = 'The input is not valid.')


def select_table(*args):
    table = sel_tab_comb.get()
    generate_table(table)


def delete_row():
    table = sel_tab_comb.get()
    confirm = messagebox.askquestion(
        message = 'Delete the latest row?')
    if confirm == 'yes':
        main.delete_row(table)
        generate_table(table)


def delete_table():
    table = sel_tab_comb.get()
    confirm = messagebox.askquestion(
        message = 'Are you sure to delete this table?')
    if confirm == 'yes':
        main.delete_table(table)
        init_ui()


def generate_table(table):
    finance_tab.delete(*finance_tab.get_children())
    all_data = main.get_tabledata(table)
    data = all_data[0]
    data_sum = all_data[1]
    for i in data:
        if not i[2]: income = ''
        else: income = "{:,}".format(i[2])
        bank   = "{:,}".format(i[3])
        wallet = "{:,}".format(i[4])
        if not i[5]: bank_dif   = ''
        else:        bank_dif   = "{:,}".format(i[5])
        if not i[6]: wallet_dif = ''
        else:        wallet_dif = "{:,}".format(i[6])
        if not i[7]: total_dif  = ''
        else:        total_dif  = "{:,}".format(i[7])
        if not i[8]: notes      = ''
        else: notes = '    {}'.format(i[8])
        finance_tab.insert(parent='', index = 'end', 
                            values = (i[1], income, bank, wallet, 
                            bank_dif, wallet_dif, total_dif, notes))
        
    finance_tab.insert(parent = '', index = 'end', 
                    values = ('--------------', '--------------',
                                '--------------', '--------------',
                                '--------------', '--------------',
                                '--------------',
                                '-------------------------------',))
    if not data_sum[0]: income_sum      = '-'
    else:               income_sum      = "{:,}".format(data_sum[0])
    if not data_sum[1]: bank_dif_sum    = '-'
    else:               bank_dif_sum    = "{:,}".format(data_sum[1])
    if not data_sum[2]: wallet_dif_sum  = '-'
    else:               wallet_dif_sum  = "{:,}".format(data_sum[2])
    if not data_sum[3]: total_dif_sum   = '-'
    else:               total_dif_sum   = "{:,}".format(data_sum[3])
    finance_tab.insert(parent = '', index = 'end', 
                        values = ('Grand Total', income_sum, '', '', 
                                    bank_dif_sum, wallet_dif_sum, 
                                    total_dif_sum, ''))


# ---------- create widget -----------

input_frm   = Frame(app, padding = 10)
date_l      = Label(input_frm, text = 'Date:')
date_ent    = DateEntry(input_frm, date_pattern = 'yyyy-MM-dd')
income_l    = Label(input_frm, text = 'Income:')
income_ent  = Entry(input_frm, width = 15)
banl_l      = Label(input_frm, text = 'Bank Remaining: *')
bank_ent    = Entry(input_frm, width = 15)
wallet_l    = Label(input_frm, text = 'Wallet Remaining: *')
wallet_ent  = Entry(input_frm, width = 15)
notes_l     = Label(input_frm, text = 'Notes:')
notes_ent   = Entry(input_frm, width = 25)
submit_btn  = Button(input_frm, text = 'Submit', width = 7, 
                     command = submit_data)

sep1 = Separator(app, orient = 'horizontal')

get_tab_frm     = Frame(app, padding = 10)
sel_tab_l       = Label(get_tab_frm, text = 'Select table:')
sel_tab_comb    = Combobox(get_tab_frm, state = 'readonly')
del_tab_btn     = Button(get_tab_frm, text = 'Delete This Table', 
                         command = delete_table)
del_row_btn     = Button(get_tab_frm, text = 'Delete Latest Row', 
                         command = delete_row)

# generate table
gen_tab_w = 80
col_list    = ('', 'Date', 'Income', 
                'Bank Remaining', 'Wallet Remaining', 
                'Bank Spending', 'Wallet Spending', 
                'Total  Spending', 'Notes')
col_w_list  = (0, 70, gen_tab_w, gen_tab_w, gen_tab_w, 
                gen_tab_w, gen_tab_w, gen_tab_w, 200)
col_an_list = (W, W, E, E, E, E, E, E, W)
finance_tab = Treeview(app, columns = col_list[1:])
for i in range(len(col_list)):
    finance_tab.column(f'#{i}', width = col_w_list[i], 
                        anchor = col_an_list[i])
    finance_tab.heading(f'#{i}', text = col_list[i])


# ---------- place widget ----------

input_frm.pack  ()
date_l.grid     (sticky = W, row = 0, column = 0, padx = 5)
date_ent.grid   (row = 1, column = 0, padx = 5)
income_l.grid   (sticky = W, row = 0, column = 1, padx = 5)
income_ent.grid (row = 1, column = 1, padx = 5)
banl_l.grid     (sticky = W, row = 0, column = 2, padx = 5)
bank_ent.grid   (row = 1, column = 2, padx = 5)
wallet_l.grid   (sticky = W, row = 0, column = 3, padx = 5)
wallet_ent.grid (row = 1, column = 3, padx = 5)
notes_l.grid    (sticky = W, row = 0, column = 4, padx = 5)
notes_ent.grid  (row = 1, column = 4, padx = 5)
submit_btn.grid (row = 1, column = 5, padx = 5)

sep1.pack       (fill = 'x')

get_tab_frm.pack    (fill = 'both')
sel_tab_l.pack      (side = 'left')
sel_tab_comb.pack   (side = 'left')
del_tab_btn.pack    (side = 'right')
del_row_btn.pack    (side = 'right', padx = 10)

finance_tab.pack (fill = 'both', expand = 1, padx = 10, pady = (0,10))

init_ui()

# ---------- validate / get events ----------

sel_tab_comb.bind("<<ComboboxSelected>>", select_table)


app.mainloop()