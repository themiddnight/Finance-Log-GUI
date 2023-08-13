from flask import Flask, render_template, request, make_response
from datetime import datetime
import base64
from matplotlib.figure import Figure
from io import BytesIO
import io
import main

app = Flask(__name__)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table/add-table', methods=['GET', 'POST'])
def addtable():
    date = request.form['date']
    table = '{} {}'.format(main.get_month_name(date.split('-')[1]),
                           date.split('-')[0])
    if request.form['income']:
        income = int(request.form['income'])
    else:
        income = None
    bank = int(request.form['bank'])
    wallet = int(request.form['wallet'])
    notes = request.form['notes']
    main.init(table)
    main.insert_data(table, date, income, bank, wallet, notes)
    table_list = main.get_tablelist()
    table_data = main.get_tabledata(table)[0]
    sum_data = main.get_tabledata(table)[1]

    return render_template('table.html', table_list=table_list,
                           table=table, date=date, income=income,
                           bank=bank, wallet=wallet, notes=notes,
                           data=table_data, sum=sum_data)


@app.route('/table/delete-row', methods=['GET', 'POST'])
def deleterow():
    table_list = main.get_tablelist()
    table = request.args['table']
    main.delete_row(table)
    table_data = main.get_tabledata(table)

    return render_template('table.html', table_list=table_list,
                           table=table, data=table_data[0], 
                           sum=table_data[1])


@app.route('/table/delete-table')
def deletetable():
    table = request.args['table']
    main.delete_table(table)
    table_list = main.get_tablelist()
    table_data = main.get_tabledata(table_list[-1])

    return render_template('table.html', table_list=table_list,
                           table=table_list[-1], data=table_data[0], 
                           sum=table_data[1])


@app.route('/table', methods=['GET', 'POST'])
def table():
    main.init(datetime.now().strftime('%B %Y'))
    table_list = main.get_tablelist()
    if request.method == 'POST':
        now_table = request.form['item']
    elif request.method == 'GET':
        now_table = datetime.now().strftime('%B %Y')
    table_data = main.get_tabledata(now_table)

    return render_template('table.html', table_list=table_list,
                           table=now_table, data=table_data[0], 
                           sum=table_data[1])


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    now_table = request.args['table']
    (day_list, income_list, bank_list, wallet_list, bank_d_list, wallet_d_list, sum_remain) = main.get_rotate_table(now_table)
    # Generate the figure **without using pyplot**.
    figure = Figure()

    ax = figure.add_subplot(211)
    ax.plot(day_list, bank_d_list, label = "Bank")
    ax.plot(day_list, wallet_d_list, label = "Wallet")
    ax.grid(linestyle = '--', linewidth = 0.3)
    ax.legend()
    ax.invert_yaxis()
    ax.tick_params(axis="both")
    ax.legend()

    ax = figure.add_subplot(212)
    ax.bar(day_list, income_list, label = "Income")
    ax.plot(day_list, sum_remain, label = "Remaining")
    ax.grid(linestyle = '--', linewidth = 0.3)
    ax.legend()
    ax.tick_params(axis="both")
    ax.legend()
    figure.subplots_adjust(left = 0.07, bottom = 0.08,
                            right = 0.95, top = 0.94)
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png")
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.mimetype = "image/png"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
