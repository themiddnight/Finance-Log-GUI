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
        self.geometry(self.controller.get_app_geo())
        self.minsize(810, 500)
        icon = PhotoImage(file = "image/icon.png")
        self.iconphoto(False, icon)


        # ---------- create widget -----------

        # select table frame
        self.get_tabl_frm  = ttk.Frame(self)
        self.sel_tabl_l    = ttk.Label(self.get_tabl_frm, text = 'Select table:')
        self.sel_tabl_comb = ttk.Combobox(self.get_tabl_frm, state = 'readonly')
        self.theme_btn     = ttk.Button(self.get_tabl_frm, text='☀︎', width = 2
                                        ,command = self.toggle_theme)
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
        self.graph_canvas = FigureCanvasTkAgg(self.figure
                                             ,master = self.graph_frm)

        # input frame
        inp_w = 18
        self.input_frm    = ttk.Labelframe(self, text = 'Insert Data:')
        self.date_l       = ttk.Label(self.input_frm, text = 'Date: *')
        self.date_ent     = DateEntry(self.input_frm,date_pattern = 'yyyy-MM-dd'
                                     ,firstweekday = 'sunday'
                                     ,showweeknumbers = False
                                     ,showothermonthdays = False
                                     ,width = inp_w)
        self.banl_l       = ttk.Label(self.input_frm, text = 'Bank Remaining: *')
        self.bank_ent     = ttk.Entry(self.input_frm, width = inp_w)
        self.cash_l       = ttk.Label(self.input_frm, text = 'Cash Remaining: *')
        self.cash_ent     = ttk.Entry(self.input_frm, width = inp_w)
        self.notes_l      = ttk.Label(self.input_frm, text = 'Notes:')
        self.notes_ent    = ttk.Entry(self.input_frm, width = inp_w)
        self.income_l     = ttk.Label(self.input_frm, text = 'Income:')
        self.income_ent   = ttk.Entry(self.input_frm, width = inp_w)
        self.withdraw_l   = ttk.Label(self.input_frm, text = 'Withdraw:')
        self.withdraw_ent = ttk.Entry(self.input_frm, width = inp_w)
        self.submit_btn   = ttk.Button(self.input_frm, text = 'Submit'
                                      ,command = self.submit_data)


        # ---------- place widget ----------

        self.get_tabl_frm.pack (fill = 'both', pady = (15, 0), padx = 20)
        self.sel_tabl_l.pack   (side = 'left')
        self.sel_tabl_comb.pack(side = 'left')
        self.theme_btn.pack    (side = 'right')
        self.del_tabl_btn.pack (side = 'right', ipadx = 10, padx = 5)
        self.del_row_btn.pack  (side = 'right', ipadx = 10)

        self.tab_view.add(self.table_frm, text = f'{"Table": ^20}') 
        self.tab_view.add(self.graph_frm, text = f'{"Graph": ^20}')
        self.tab_view.pack(fill = 'both', expand = 1, pady = 5)

        self.scrl_table.pack  (side = 'right', fill = 'y')
        self.finance_tabl.pack(fill = 'both', expand = 1)

        self.graph_canvas.get_tk_widget().pack(expand = 1, fill = 'both')

        self.input_frm.pack   (padx = 20, pady = (0, 30), ipadx = 5, ipady = 5)
        self.date_l.grid      (row=0, column=0, padx=10, sticky='w', pady=(5,0))
        self.date_ent.grid    (row=1, column=0, padx=10)
        self.banl_l.grid      (row=0, column=1, padx=10, sticky='w', pady=(5,0))
        self.bank_ent.grid    (row=1, column=1, padx=10)
        self.cash_l.grid      (row=0, column=2, padx=10, sticky='w', pady=(5,0))
        self.cash_ent.grid    (row=1, column=2, padx=10)

        self.income_l.grid    (row=2, column=0, padx=10, sticky='w')
        self.income_ent.grid  (row=3, column=0, padx=10)
        self.withdraw_l.grid  (row=2, column=1, padx=10, sticky='w')
        self.withdraw_ent.grid(row=3, column=1, padx=10)
        self.notes_l.grid     (row=2, column=2, padx=10, sticky='w')
        self.notes_ent.grid   (row=3, column=2, padx=10)

        self.submit_btn.grid  (row=0, column=3, padx=10, sticky='ns',pady = (10,0)
                               ,ipadx=20, rowspan=4)


        # ---------- bindings ----------

        self.bind('<Configure>', self.save_screen_size)
        self.bank_ent.bind('<Return>', self.submit_data)
        self.cash_ent.bind('<Return>', self.submit_data)
        self.notes_ent.bind('<Return>', self.submit_data)
        self.income_ent.bind('<Return>', self.submit_data)
        self.withdraw_ent.bind('<Return>', self.submit_data)
        self.sel_tabl_comb.bind("<<ComboboxSelected>>", self.select_table)
        self.finance_tabl.bind("<Double-1>", self.edit_table_win)


         # ---------- methods ----------

    def refresh_ui(self, *args):
        self.theme_sel = self.controller.get_app_theme()
        self.theme_color = self.theme_list[self.theme_sel]
        table_list = self.controller.get_table_list()
        self.sel_tabl_comb['values'] = table_list
        table = self.controller.get_current_table()
        self.sel_tabl_comb.current(table_list.index(table))
        self.generate_table_graph()
        self.focus_force()


    def generate_table_graph(self):
            table = self.finance_tabl
            data = self.controller.get_table_data()
            data_sum = self.controller.get_table_sum()
            table = TableGenerate(table, data, data_sum)
            table.generate()

            figure = self.figure
            canvas = self.graph_canvas
            theme = self.theme_color
            cols_data, sum_remain = self.controller.get_rotate_table()
            graph = GraphGenerate(figure, canvas, theme, cols_data, sum_remain)
            graph.generate()


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


    def submit_data(self, *args):
        date     = self.date_ent.get_date().strftime("%Y-%m-%d")
        income   = self.income_ent.get()
        bank     = self.bank_ent.get()
        cash     = self.cash_ent.get()
        withdraw = self.withdraw_ent.get()
        notes    = self.notes_ent.get()
        check    = self.controller.submit_data(date, income, bank, cash, 
                                               withdraw, notes)
        focused  = self.focus_get()
        if check:
            self.income_ent.delete(0, 'end')
            self.bank_ent.delete(0, 'end')
            self.cash_ent.delete(0, 'end')
            self.withdraw_ent.delete(0, 'end')
            self.notes_ent.delete(0, 'end')
            self.refresh_ui()
        else:
            messagebox.showerror(
                title = 'Value is not valid!',
                message = 'Please check your input.')
            self.focus()
            focused.focus()


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
        if self.finance_tabl.focus().isnumeric() == True: # check by row's id
            edit_window = UIedit(self, self.controller)
            edit_window.transient(self)
            edit_window.grab_set()


class TableGenerate:
    def __init__(self, table, data, data_sum):
        self.table = table
        self.data = data
        self.data_sum = data_sum

    def generate(self):
        self.table.delete(*self.table.get_children())
        for i in self.data:
            self.table.insert(
                parent = '', index = 'end', iid = i[0],
                values = (i[1], i[2], i[3], i[4]
                          ,i[5], i[6], i[7], i[8]))
        sep = 17
        self.table.insert(
            parent = '', index = 'end', 
            values = ('-' * sep, '-' * sep, '-' * sep, '-' * sep
                      ,'-' * sep, '-' * sep, '-' * sep, '-' * sep *2))
        self.table.insert(
            parent = '', index = 'end', 
            values = ('Grand Total', self.data_sum[0], '', ''
                      ,self.data_sum[1], self.data_sum[2]
                      ,self.data_sum[3], ''))


class GraphGenerate:
    def __init__(self, figure, canvas, theme, cols_data, sum_remain):
            self.figure = figure
            self.graph_canvas = canvas
            self.theme_color = theme
            # [day, income, bank, cash, bank_d, cash_d, sum_d, notes]
            self.cols_data = cols_data
            self.sum_remain = sum_remain

    def generate(self):
        self.figure.clear()
        self.graph_canvas.get_tk_widget().configure(
            background = self.theme_color["figure_bg"])
        self.figure.set_facecolor(self.theme_color["figure_bg"])
        self.figure.subplots_adjust(left = 0.07, bottom = 0.08
                                    ,right = 0.94, top = 0.94)
        
        ax1 = self.figure.add_subplot(
            211, facecolor = self.theme_color["figure_facecolor"])
        ax1.margins(x = 0.02)
        ax1.fill_between(self.cols_data[0], self.cols_data[6], 0, label = "Summary"
                        ,color = 'tab:gray', alpha = 0.2)
        ax1.plot(self.cols_data[0], self.cols_data[4]
                 ,label = "Bank", color = 'tab:blue')
        ax1.plot(self.cols_data[0], self.cols_data[5]
                 ,label = "Cash", color = 'tab:orange')
        ax1.grid(linewidth = 0.5, color = self.theme_color["grid"])
        ax1.tick_params(axis = "both"
                        ,colors = self.theme_color["tick"], labelsize = 8)
        for i in ax1.spines:
            ax1.spines[i].set_color(self.theme_color["spines"])
        ax1.set_ylabel('Spending'
                        ,color = self.theme_color["ylabel"], labelpad = 14)
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.label.set_size(9)
        ax1.legend(fontsize = 9, draggable = True
                   ,labelcolor = self.theme_color["legend"]["labelcolor"]
                   ,facecolor = self.theme_color["legend"]["facecolor"]
                   ,edgecolor = self.theme_color["legend"]["edgecolor"])
        ax1.invert_yaxis()

        ax2 = self.figure.add_subplot(
            212, sharex = ax1, facecolor = self.theme_color["figure_facecolor"])
        ax2.fill_between(self.cols_data[0], self.sum_remain,0 
                ,label = "Remaining", color = 'tab:purple', alpha=0.2)
        ax2.bar(self.cols_data[0], self.cols_data[1], zorder=3, label = "Income"
                ,alpha = 0.5, color = 'tab:cyan')
        ax2.grid(linewidth = 0.5, zorder = 0, color = self.theme_color["grid"])
        ax2.tick_params(axis = "both" 
                        ,colors = self.theme_color["tick"], labelsize = 8)
        for i in ax2.spines:
            ax2.spines[i].set_color(self.theme_color["spines"])
        ax2.set_ylabel('Income\n& Remaining'
                       ,color = self.theme_color["ylabel"], labelpad = 9)
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.label.set_size(9)
        ax2.legend(fontsize = 9, draggable = True
                   ,labelcolor = self.theme_color["legend"]["labelcolor"]
                   ,facecolor = self.theme_color["legend"]["facecolor"]
                   ,edgecolor = self.theme_color["legend"]["edgecolor"])
        for i in range(len(self.cols_data[0])):
            ax2.annotate(self.cols_data[7][i], xy = (i, 0), xytext = (-5,10)
                        ,textcoords = 'offset points', rotation = 70
                        ,fontsize = 9, fontname = 'Tahoma'
                        ,color = self.theme_color["legend"]["labelcolor"])
            
        self.graph_canvas.draw()

        
class UIedit(Toplevel):
    def __init__(self, mainview, controller):
        super().__init__()
        self.mainview   = mainview
        self.controller = controller
        
        self.sel_id = self.mainview.finance_tabl.focus()
        sel         = self.mainview.finance_tabl.item(self.sel_id)
        date, _, _, _, _, _, _, notes = sel.get("values")
        ymd_list    = date.split('-')
        day         = ymd_list.pop(2)
        self.ym_str = '-'.join(ymd_list) + '-'

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
        self.geometry(f'550x100+{main_cen_x - 275}+{main_cen_y - 50}')
        self.minsize (550, 100)
    
        self.edit_frm       = ttk.Frame(self)
        self.date_l         = ttk.Label(self.edit_frm,text='Date:')
        self.date_frm       = ttk.Frame(self.edit_frm)
        self.yyyymm_l       = ttk.Label(self.date_frm, text = self.ym_str)
        self.edit_day_ent   = ttk.Spinbox(self.date_frm, width = 3
                                         ,from_ = 1, to = 31, wrap = True)
        self.edit_notes_l   = ttk.Label(self.edit_frm, text = 'Notes: ')
        self.edit_notes_ent = ttk.Entry(self.edit_frm, width = 40)
        submit_btn          = ttk.Button(self, text = 'Submit'
                                        ,command = self.submit_edit)

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
        if day_new.isnumeric() == True:
            date_new  = self.ym_str + "{:02}".format(int(day_new))
            notes_new = self.edit_notes_ent.get()
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