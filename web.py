from flask import Flask, render_template, request
from datetime import datetime
import main

app = Flask(__name__)

months_name = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"december"}

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table/add-table', methods = ['GET', 'POST'])
def addtable():
    date       = request.form['date']
    table      = '{} {}'.format(months_name[date.split('-')[1]], date.split('-')[0])
    if request.form['income']: income = int(request.form['income'])
    else: income = None
    bank       = int(request.form['bank'])
    wallet     = int(request.form['wallet'])
    notes      = request.form['notes']
    main.init(table)
    main.insert_data(table, date, income, bank, wallet, notes)
    table_list = main.get_tablelist()
    table_data = main.get_tabledata(table)[0]
    sum_data   = main.get_tabledata(table)[1]

    return render_template('table.html', table_list=table_list, table=table, date=date, income=income, bank=bank, wallet=wallet, notes=notes, data=table_data, sum=sum_data)

@app.route('/table/delete-row', methods = ['GET', 'POST'])
def deleterow():
    table_list = main.get_tablelist()
    table      = request.args['table']
    main.delete_row(table)
    table_data = main.get_tabledata(table)

    return render_template('table.html', table_list=table_list, table=table,data=table_data[0], sum=table_data[1])

@app.route('/table/delete-table')
def deletetable():
    table = request.args['table']
    main.delete_table(table)
    table_list = main.get_tablelist()
    table_data = main.get_tabledata(table_list[-1])

    return render_template('table.html', table_list=table_list, table=table_list[-1],data=table_data[0], sum=table_data[1])

@app.route('/table', methods = ['GET', 'POST'])
def table():
    main.init(datetime.now().strftime('%B %Y'))
    table_list = main.get_tablelist()
    if request.method == 'POST':
        now_table = request.form['item']
    elif request.method == 'GET':
        now_table = datetime.now().strftime('%B %Y')
    table_data = main.get_tabledata(now_table)
    return render_template('table.html', table_list=table_list, table=now_table,data=table_data[0], sum=table_data[1])

if __name__ == '__main__':
    app.run(debug=True)