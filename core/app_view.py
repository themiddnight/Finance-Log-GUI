import tkinter.ttk as ttk
from tkinter import Tk, messagebox, PhotoImage, Toplevel
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UIview(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.theme_list = self.controller.get_theme_list()

        self.title('Finance Logging')
        self.minsize(1124, 430)
        icon = PhotoImage(file = "core/image/icon.png")
        self.iconphoto(False, icon)


        # ---------- create widget -----------

        # select table frame
        self.get_tabl_frm  = ttk.Frame(self)
        self.sel_tabl_l    = ttk.Label(self.get_tabl_frm, text = 'Select table:')
        self.sel_tabl_comb = ttk.Combobox(self.get_tabl_frm, state = 'readonly')
        self.theme_btn = ttk.Button(self.get_tabl_frm, text='☀︎', width = 2,
                                        command = self.toggle_theme)
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

        # input frame
        inp_w = 18
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
        self.theme_btn.pack(side = 'right')
        self.del_tabl_btn.pack (side = 'right', ipadx = 10, padx = 5)
        self.del_row_btn.pack  (side = 'right', ipadx = 10)

        self.tab_view.add(self.table_frm, text = f'{"Table": ^20}') 
        self.tab_view.add(self.graph_frm, text = f'{"Graph": ^20}')
        self.tab_view.pack(fill = 'both', expand = 1, pady = 5)

        self.scrl_table.pack  (side = 'right', fill = 'y')
        self.finance_tabl.pack(fill = 'both', expand = 1)

        self.graph_canvas.get_tk_widget().pack(expand = 1, fill = 'both')

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
        self.submit_btn.grid(row = 1, column = 5, padx = 5, ipadx = 10)


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
        self.theme_sel = self.controller.get_app_theme()
        self.theme = self.theme_list[self.theme_sel]

        self.geometry(self.controller.get_app_geo())
        table_list = self.controller.get_table_list()
        self.sel_tabl_comb['values'] = table_list
        table = self.controller.get_current_table()
        self.sel_tabl_comb.current(table_list.index(table))
        self.generate_table()
        self.generate_graph()
        self.focus_force()


    def save_screen_size(self, *args):
        self.controller.save_app_geo(self.geometry())

    
    def toggle_theme(self, *args):
        if self.theme_sel == "bright":
            self.theme_sel = "dark"
            self.controller.save_app_theme("dark")
        elif self.theme_sel == "dark":
            self.theme_sel = "bright"
            self.controller.save_app_theme("bright")
        self.refresh_ui()


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
        sep = 17
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
        self.graph_canvas.get_tk_widget().configure(background = self.theme["figure_bg"])
        self.figure.set_facecolor(self.theme["figure_bg"])
        self.figure.subplots_adjust(left = 0.07, bottom = 0.08,
                                    right = 0.94, top = 0.94)
        
        ax1 = self.figure.add_subplot(211, facecolor = self.theme["figure_facecolor"])
        ax1.fill_between(cols_data[0], cols_data[6], 0, label = "Summary", 
                        color = 'tab:gray', alpha = 0.3)
        ax1.plot(cols_data[0], cols_data[4], label = "Bank", color = 'tab:blue')
        ax1.plot(cols_data[0], cols_data[5], label = "Cash", color = 'tab:orange')
        ax1.grid(linewidth = 0.5, color = self.theme["grid"])
        ax1.tick_params(axis = "both", colors = self.theme["tick"], labelsize = 8)
        for i in ax1.spines:
            ax1.spines[i].set_color(self.theme["spines"])
        ax1.set_ylabel('Spending', color = self.theme["ylabel"], labelpad = 14)
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.label.set_size(9)
        ax1.legend(fontsize = 9, draggable = True, 
                   labelcolor = self.theme["legend"]["labelcolor"], 
                   facecolor = self.theme["legend"]["facecolor"], 
                   edgecolor = self.theme["legend"]["edgecolor"])
        try:
            max_spnd = min(cols_data[6])
            ax1.set_ylim(top = 0, bottom = max_spnd + (max_spnd*0.05))
        except:
            pass
        ax1.invert_yaxis()

        ax2 = self.figure.add_subplot(212, facecolor = self.theme["figure_facecolor"])
        ax2.bar(cols_data[0], cols_data[1], label = "Income", 
               alpha = 0.3, color = 'tab:cyan')
        ax2.plot(cols_data[0], sum_remain, label = "Remaining", color = 'tab:purple')
        ax2.grid(linewidth = 0.5, color = self.theme["grid"])
        ax2.tick_params(axis = "both", colors = self.theme["tick"], labelsize = 8)
        for i in ax2.spines:
            ax2.spines[i].set_color(self.theme["spines"])
        ax2.set_ylabel('Income\n& Remaining', color = self.theme["ylabel"], labelpad = 9)
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.label.set_size(9)
        ax2.legend(fontsize = 9, draggable = True, 
                   labelcolor = self.theme["legend"]["labelcolor"], 
                   facecolor = self.theme["legend"]["facecolor"], 
                   edgecolor = self.theme["legend"]["edgecolor"])
        for i in range(len(cols_data[0])):
            ax2.annotate(cols_data[7][i], xy = (i, 0), xytext = (-5,10)
                        ,textcoords = 'offset points', rotation = 60
                        ,fontsize = 10, fontname = 'Tahoma'
                        ,color = self.theme["legend"]["labelcolor"])
            
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
        if self.finance_tabl.focus().isnumeric() == True:
            edit_window = UIedit(self, self.controller)
            edit_window.transient(self)
            edit_window.grab_set()

        
class UIedit(Toplevel):
    def __init__(self, mainview, controller):
        super().__init__()

        self.mainview = mainview
        self.controller = controller
        
        self.sel_id = self.mainview.finance_tabl.focus()
        sel         = self.mainview.finance_tabl.item(self.sel_id)
        date, _, _, _, _, _, _, notes = sel.get("values")
        ymd_list = date.split('-')
        day      = ymd_list.pop(2)
        self.ym_str   = '-'.join(ymd_list) + '-'

        # to make edit ui centered to the main ui
        main_geo   = self.mainview.geometry()
        dimensions = []
        for part in main_geo.split('x'):
            dimensions.extend([int(dim) for dim in part.split('+')])
        main_w, main_h, main_x, main_y = dimensions
        main_cen_x = round(main_x + (main_w / 2))
        main_cen_y = round(main_y + (main_h / 2))

        # generate ui
        self.focus_force()
        self.title   (f'Edit: {date}')
        self.geometry('550x100+{}+{}'.format(main_cen_x - 275, main_cen_y - 50))
        self.minsize (550, 100)
    
        self.edit_frm       = ttk.Frame(self)
        self.date_l         = ttk.Label(self.edit_frm,text='Date:')
        self.date_frm       = ttk.Frame(self.edit_frm)
        self.yyyymm_l       = ttk.Label(self.date_frm, text = self.ym_str)
        self.edit_day_ent   = ttk.Spinbox(self.date_frm, width = 3, 
                                          from_ = 1, to = 31, wrap = True)
        self.edit_notes_l   = ttk.Label(self.edit_frm, text = 'Notes: ')
        self.edit_notes_ent = ttk.Entry(self.edit_frm, width = 40)
        submit_btn          = ttk.Button(self, text = 'Submit', 
                                         command = self.submit_edit)

        self.edit_day_ent.insert(0, day)
        self.edit_notes_ent.insert(0, notes[2:])

        self.edit_frm.pack      (padx = 10, pady = (10, 5))
        self.date_l.grid        (sticky = 'w',row = 0, column = 0)
        self.date_frm.grid      (sticky = 'w',row = 1, column = 0, padx = (0, 10))
        self.yyyymm_l.pack      (side = 'left')
        self.edit_day_ent.pack  (side = 'left')
        self.edit_notes_l.grid  (sticky = 'w', row = 0, column = 1, padx = 5)
        self.edit_notes_ent.grid(row = 1, column = 1, padx = 5)
        submit_btn.pack         (pady = (0, 10))

        self.edit_day_ent.bind('<Return>', self.submit_edit)
        self.edit_notes_ent.bind('<Return>', self.submit_edit)


    def submit_edit(self, *args):
        day_new   = self.edit_day_ent.get()
        date_new  = self.ym_str + "{:02d}".format(int(day_new))
        notes_new = self.edit_notes_ent.get()
        if day_new.isnumeric() == True:
            self.controller.edit_row(self.sel_id, date_new, notes_new)
            self.destroy()
            self.mainview.refresh_ui()
        else:
            messagebox.showerror(
                title = 'Value is not valid!',
                message = 'Please check your date input.')
            self.edit_day_ent.focus_force()
    

if __name__ == "__main__":
    import app_controller
    app = app_controller.Controller()
    app.run()
