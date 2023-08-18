import tkinter.ttk as ttk
from tkinter import Tk, messagebox, PhotoImage, Toplevel
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UIView(Tk):
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        self.edit_win = None

        self.title('Finance Logging')
        self.minsize(1000, 430)
        photo = PhotoImage(file = "core/image/icon.png")
        self.iconphoto(False, photo)

        self.style = ttk.Style()
        self.style.configure('TEntry', background = None)


        # ---------- create widget -----------

        # select table
        self.get_tabl_frm  = ttk.Frame(self)
        self.sel_tabl_l    = ttk.Label(self.get_tabl_frm, text = 'Select table:')
        self.sel_tabl_comb = ttk.Combobox(self.get_tabl_frm, state = 'readonly')
        self.del_tabl_btn  = ttk.Button(self.get_tabl_frm, text = 'Delete This Table'
                                        ,command = self.delete_table)
        self.del_row_btn   = ttk.Button(self.get_tabl_frm, text = 'Delete Latest Row'
                                        ,command = self.delete_row)
        # create tab
        self.tab_view  = ttk.Notebook(self)
        self.table_frm = ttk.Frame(self.tab_view)
        self.graph_frm = ttk.Frame(self.tab_view)

        # generate table head
        gen_tabl_w  = 80
        col_list    = ('', 'Date', 'Income', 
                        'Bank Remaining', 'Cash Remaining', 
                        'Bank Spending', 'Cash Spending', 
                        'Total  Spending', 'Notes')
        col_w_list  = (0, 70, gen_tabl_w, gen_tabl_w, gen_tabl_w, 
                        gen_tabl_w, gen_tabl_w, gen_tabl_w, 200)
        col_al_list = ('w', 'w', 'e', 'e', 'e', 'e', 'e', 'e', 'w')
        self.scrl_table   = ttk.Scrollbar(self.table_frm)
        self.finance_tabl = ttk.Treeview(self.table_frm, columns = col_list[1:]
                                         ,yscrollcommand = self.scrl_table.set)
        for i in range(len(col_list)):
            self.finance_tabl.column(f'#{i}', width = col_w_list[i]
                                     ,anchor = col_al_list[i])
            self.finance_tabl.heading(f'#{i}', text = col_list[i])

        # generate graph canvas
        self.figure       = Figure(figsize = (6, 2), facecolor = "#222222")
        self.graph_canvas = FigureCanvasTkAgg(self.figure, master = self.graph_frm)
        self.graph_canvas.get_tk_widget().configure(background = "#222222")

        # input
        # self.input_ttl_l = ttk.Label(text = 'Insert Data:')
        inp_w = 14
        self.input_frm   = ttk.Labelframe(self, text = 'Insert Data:')
        self.date_l      = ttk.Label(self.input_frm, text = 'Date: *')
        self.date_ent    = DateEntry(self.input_frm, date_pattern = 'yyyy-MM-dd'
                                     ,firstweekday = 'sunday'
                                     ,showweeknumbers = False
                                     ,showothermonthdays = False)
        self.income_l    = ttk.Label(self.input_frm, text = 'Income:')
        self.income_ent  = ttk.Entry(self.input_frm, width = inp_w)
        self.banl_l      = ttk.Label(self.input_frm, text = 'Bank Remaining: *')
        self.bank_ent    = ttk.Entry(self.input_frm, width = inp_w)
        self.cash_l      = ttk.Label(self.input_frm, text = 'Cash Remaining: *')
        self.cash_ent    = ttk.Entry(self.input_frm, width = inp_w)
        self.notes_l     = ttk.Label(self.input_frm, text = 'Notes:')
        self.notes_ent   = ttk.Entry(self.input_frm, width = 24)
        self.submit_btn  = ttk.Button(self.input_frm, text = 'Submit'
                                      ,width = 7, command = self.submit_data)


        # ---------- place widget ----------

        self.get_tabl_frm.pack (fill = 'both', pady = (15, 0), padx = 20)
        self.sel_tabl_l.pack   (side = 'left')
        self.sel_tabl_comb.pack(side = 'left')
        self.del_tabl_btn.pack (side = 'right')
        self.del_row_btn.pack  (side = 'right', padx = 10)

        self.tab_view.add(self.table_frm, text = 'Table')
        self.tab_view.add(self.graph_frm, text = 'Graph')
        self.tab_view.pack(fill = 'both', expand = 1)

        self.scrl_table.pack  (side = 'right', fill = 'y')
        self.finance_tabl.pack(fill = 'both', expand = 1)

        self.graph_canvas.get_tk_widget().pack(expand = 1, fill = 'both')

        # self.input_ttl_l.pack(anchor = 'nw', padx = 12, pady = (0, 5))
        self.input_frm.pack (padx = 20, pady = (0, 20), ipadx = 5, ipady = 3)
        self.date_l.grid    (sticky='w', row=0, column=0, padx=5, pady=(5,0))
        self.date_ent.grid  (row = 1, column = 0, padx = 5)
        self.income_l.grid  (sticky='w', row=0, column=1, padx=5, pady=(5,0))
        self.income_ent.grid(row = 1, column = 1, padx = 5)
        self.banl_l.grid    (sticky='w', row=0, column=2, padx=5, pady=(5,0))
        self.bank_ent.grid  (row = 1, column = 2, padx = 5)
        self.cash_l.grid    (sticky='w', row=0, column=3, padx=5, pady=(5,0))
        self.cash_ent.grid  (row = 1, column = 3, padx = 5)
        self.notes_l.grid   (sticky='w', row=0, column=4, padx=5, pady=(5,0))
        self.notes_ent.grid (row = 1, column = 4, padx = 5)
        self.submit_btn.grid(row = 1, column = 5, padx = 5)


        # ---------- validate / get events ----------

        self.bind('<Configure>', self.save_screen_size)
        self.income_ent.bind('<Return>', self.submit_data)
        self.bank_ent.bind('<Return>', self.submit_data)
        self.cash_ent.bind('<Return>', self.submit_data)
        self.notes_ent.bind('<Return>', self.submit_data)
        self.sel_tabl_comb.bind("<<ComboboxSelected>>", self.select_table)
        self.finance_tabl.bind("<Double-1>", self.edit_table_win)


         # ---------- methods ----------

    def refresh_ui(self, *args):
        self.geometry(self.controller.get_app_geo())
        table_list = self.controller.get_table_list()
        self.sel_tabl_comb['values'] = table_list
        table = self.controller.get_current_table()
        self.sel_tabl_comb.current(table_list.index(table))
        self.generate_table()
        self.generate_graph()
        self.focus_force()


    def save_screen_size(self, *args):
        self.controller.save_screen_size(self.geometry())


    def select_table(self, *args):
        table = self.sel_tabl_comb.get()
        self.controller.set_current_table(table)
        self.refresh_ui()


    def generate_table(self):
        self.finance_tabl.delete(*self.finance_tabl.get_children())
        data     = self.controller.get_table_data()
        data_sum = self.controller.get_table_sum()
        for i in data:
            self.finance_tabl.insert(
                parent = '', index = 'end', iid = i[0],
                values = (i[1], i[2], i[3], i[4]
                          ,i[5], i[6], i[7], i[8]))
        sep = 15
        self.finance_tabl.insert(
            parent = '', index = 'end', 
            values = ('-' * sep, '-' * sep, '-' * sep, '-' * sep
                      ,'-' * sep, '-' * sep, '-' * sep, '-' * sep *2))
        self.finance_tabl.insert(
            parent = '', index = 'end', 
            values = ('Grand Total', data_sum[0], '', ''
                      ,data_sum[1], data_sum[2], data_sum[3], ''))


    def generate_graph(self):
        # [day, income, bank, cash, bank_d, cash_d, sum_d, notes], sum_remain
        cols_data, sum_remain = self.controller.get_rotate_table()
        self.figure.clear()
        max_spnd = min(cols_data[6])
        ax = self.figure.add_subplot(211, facecolor = '#131313')
        ax.plot(cols_data[0], cols_data[6], label = "Summary", color = '#383838')
        ax.fill_between(cols_data[0], cols_data[6],0, color = '#383838')
        ax.plot(cols_data[0], cols_data[4], label = "Bank")
        ax.plot(cols_data[0], cols_data[5], label = "Cash")
        ax.grid(linestyle = '--', linewidth = 0.1)
        ax.set_ylim(top = 0, bottom = max_spnd + (max_spnd*0.05))
        ax.invert_yaxis()
        ax.tick_params(axis = "both", colors = "white", labelsize = 8)
        ax.set_ylabel('Spending', color = 'white', labelpad = 14)
        ax.yaxis.label.set_size(9)
        ax.yaxis.set_label_position("right")
        ax.legend(fontsize = 9, labelcolor = 'white', 
                  facecolor = "#333333", edgecolor = "#444444")

        ax = self.figure.add_subplot(212, facecolor = '#131313')
        ax.bar(cols_data[0], cols_data[1], label = "Income", alpha = 0.3)
        ax.plot(cols_data[0], sum_remain, label = "Remaining")
        ax.grid(linestyle = '--', linewidth = 0.1)
        ax.tick_params(axis = "both", colors = "white", labelsize = 8)
        ax.set_ylabel('Income\n& Remaining', color = 'white', labelpad = 9)
        ax.yaxis.set_label_position("right")
        ax.yaxis.label.set_size(9)
        ax.legend(fontsize = 9, labelcolor = 'white', 
                  facecolor = "#333333", edgecolor = "#444444")
        self.figure.subplots_adjust(left = 0.07, bottom = 0.08,
                                right = 0.94, top = 0.94)
        
        for i in range(len(cols_data[0])):
            ax.annotate(cols_data[7][i], xy = (i, 0), xytext = (-5,10)
                        ,textcoords = 'offset points', rotation = 60
                        ,fontsize = 10, fontname = 'Tahoma', color = '#cccccc')
            
        self.graph_canvas.draw()


    def submit_data(self, *args):
        date   = self.date_ent.get_date().strftime("%Y-%m-%d")
        income = self.income_ent.get()
        bank   = self.bank_ent.get()
        cash   = self.cash_ent.get()
        notes  = self.notes_ent.get()
        check  = self.controller.submit_data(date, income, bank, cash, notes)
        if check == False:
            messagebox.showerror(title = 'Value is not valid!'
                                 ,message = 'Please check your input.')
        else:
            self.income_ent.delete(0, 'end')
            self.bank_ent.delete(0, 'end')
            self.cash_ent.delete(0, 'end')
            self.notes_ent.delete(0, 'end')
            self.refresh_ui()


    def delete_row(self, *args):
        confirm = messagebox.askyesno(
            title   = 'Delete Latest Row',
            message = 'Do you want to delete the latest row?')
        if confirm == True:
            self.controller.delete_row()
        self.refresh_ui()


    def delete_table(self, *args):
        confirm = messagebox.askyesno(
            title   = 'Delete Table',
            message = 'Are you sure to delete this table?')
        if confirm == True:
            self.controller.delete_table()
        self.refresh_ui()


    def edit_table_win(self, *args):
        self.sel_id = self.finance_tabl.focus()
        sel = self.finance_tabl.item(self.sel_id)
        date, _, _, _, _, _, _, notes = sel.get("values")
        yyyymmdd = date.split('-')
        day      = yyyymmdd.pop(2)
        yyyymm   = '-'.join(yyyymmdd)
        main_geo = self.geometry()
        dimensions = []
        for part in main_geo.split('x'):
            dimensions.extend([int(dim) for dim in part.split('+')])
        main_w, main_h, main_x, main_y = dimensions
        main_cen_x = round(main_x + (main_w / 2))
        main_cen_y = round(main_y + (main_h / 2))

        # generate ui
        if self.edit_win:
            self.edit_win.destroy()
        self.edit_win = Toplevel(self)
        self.edit_win.attributes('-topmost', 'true')
        self.edit_win.resizable(False, False)

        self.edit_win.title(f'Edit: {date}')
        self.edit_win.geometry('550x100+{}+{}'.format
                               (main_cen_x - 275, main_cen_y - 50))
        self.edit_win.minsize(550, 100)
    
        self.edit_frm = ttk.Frame(self.edit_win)
        self.edit_frm.pack(padx = 10, pady = (10, 5))
        ttk.Label(self.edit_frm,text='Date:').grid(
            sticky = 'w',row = 0, column = 0)
        self.date_frm = ttk.Frame(self.edit_frm)
        self.date_frm.grid(
            sticky = 'w',row = 1, column = 0, padx = (0, 10))
        self.yyyymm = ttk.Label(self.date_frm, text = yyyymm + '-')
        self.yyyymm.pack(side = 'left')
        self.edit_day_ent = ttk.Entry(self.date_frm, width = 3)
        self.edit_day_ent.pack(side = 'left')
        self.edit_day_ent.insert(0, day)
        ttk.Label(self.edit_frm, text = 'Notes: ').grid(
            sticky = 'w', row = 0, column = 1, padx = 5)
        self.edit_notes_ent = ttk.Entry(self.edit_frm, width = 40)
        self.edit_notes_ent.grid(row = 1, column = 1, padx = 5)
        self.edit_notes_ent.insert(0, notes[2:])
        submit_btn = ttk.Button(self.edit_win, text = 'Submit'
                                ,command = self.submit_edit)
        submit_btn.pack(pady = (0, 10))

        self.edit_day_ent.bind('<Return>', self.submit_edit)
        self.edit_notes_ent.bind('<Return>', self.submit_edit)
        # self.edit_win.bind('<Button-1>', self.lift())


    def submit_edit(self, *args):
        yyyymm    = self.yyyymm["text"]
        day_new = self.edit_day_ent.get()
        date_new  = yyyymm + day_new
        notes_new = self.edit_notes_ent.get()
        if day_new.isnumeric() == True:
            self.controller.edit_row(self.sel_id, date_new, notes_new)
            self.edit_win.destroy()
            self.refresh_ui()
        else:
            messagebox.showerror(
                title = 'Value is not valid!',
                message = 'Please check your date input.')
            self.edit_day_ent.focus_force()
        

if __name__ == "__main__":
    import app_controller
    app = app_controller.Controller()
    app.run()