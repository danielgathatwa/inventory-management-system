from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from configs import Development
import collections
import pygal

# flask object
app = Flask(__name__)

app.config.from_object(Development)

# sql_alchemy instance
db = SQLAlchemy(app)

from models.inventories import InventoryModel
from models.sales import SalesModel


@app.before_first_request
def create_tables():
    # db.drop_all()
    db.create_all()


# Home Page
@app.route('/', methods=['GET'])
def home():
    try:
        pie_chart = pygal.Pie()
        pie_chart.title = 'Inventory Type'
        pie_chart.add('Products', InventoryModel.getTypeCount('Product'))
        pie_chart.add('Services', InventoryModel.getTypeCount('Service'))

        pie_data = pie_chart.render_data_uri()
        return render_template("index.html", pietype=pie_data)
    except:
        return render_template('index.html')


# Inventory Page
@app.route('/inv', methods=['GET', 'POST'])
def inv():
    if request.method == 'POST':
        iname = request.form['name']
        itype = request.form['type']
        ibuying_price = request.form['bp']
        iselling_price = request.form['sp']
        istock = request.form['stock']
        ireorder_point = request.form['rp']

        entries = InventoryModel(invname=iname, invtype=itype, bp=ibuying_price, sp=iselling_price, stock=istock,
                                 rp=ireorder_point)
        db.session.add(entries)
        db.session.commit()
        print("Successfully added")

    all_entries = InventoryModel.query.all()

    return render_template('inv.html', invs=all_entries)


# about page
@app.route('/about')
def about():
    return render_template('about.html')


# charting page
@app.route('/charting',methods=['POST','GET'])
def charting():
    sales_record = SalesModel.query.join(InventoryModel).add_columns(SalesModel.created_at, SalesModel.id,
                                                                     InventoryModel.invname,
                                                                     InventoryModel.invtype, InventoryModel.sp,
                                                                     SalesModel.qty)
    date_list = {}
    date_parameters = '2018'
    chart_type = 'Line'
    if request.method == 'POST':
        date_parameters = request.form['year']
        chart_type = request.form['chart_type']
    for record in sales_record:
        date_record = record.created_at
        date = str(date_record.date())
        if date[:4] == date_parameters:
            if date[5:7] in date_list:
                date_list[date[5:7]] += (record.sp * record.qty)
            else:
                date_list[date[5:7]] = record.sp * record.qty
        else:
            pass

    ordered_list = collections.OrderedDict(sorted(date_list.items()))
    x_labels = []
    sales = []
    for key in ordered_list:
        x_labels.append(key)
        sales.append(date_list[key])
    try:
        if chart_type == 'Line':
            line_chart = pygal.Line()
        elif chart_type == 'Bar':
            line_chart = pygal.Bar()
        elif chart_type == 'Pie':
            line_chart = pygal.Pie()
        else:
            line_chart = pygal.Line()
        line_chart.title = 'Daily total sales {}'.format(date_parameters)
        line_chart.x_labels = x_labels
        line_chart.add('Total Sales', sales)

        line_data = line_chart.render_data_uri()
        return render_template("charting.html", linetype_date=line_data)

    except:
        return render_template('charting.html')


# sales modal
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        sales_qty = request.form['qty']
        foreign_id = request.form['inventory_id']

        if InventoryModel.update_stock(foreign_id, int(sales_qty)):
            print('stock update success')
        else:
            flash('Error, the quantity of sales entered is greater than stock available', 'danger')
        sales = SalesModel(inv_id=foreign_id, qty=sales_qty)
        db.session.add(sales)
        db.session.commit()
        print('sales saved')

    return redirect(url_for('inv'))


# Edit inventory modal
@app.route('/edit-inv', methods=['GET', 'POST'])
def edit_inv():
    if request.method == 'POST':
        inv_id = request.form['inventory_id']
        iname = request.form['name']
        itype = request.form['type']
        ibuying_price = request.form['bp']
        iselling_price = request.form['sp']
        istock = request.form['stock']
        ireorder_point = request.form['rp']

        if InventoryModel.update_inventory(id=int(inv_id), invname=iname, invtype=itype, bp=float(ibuying_price),
                                           sp=float(iselling_price), stock=int(istock), rp=int(ireorder_point)):
            print('stock update success')
        else:
            flash('Error, Fail', 'danger')
            print('error Fail')

    return redirect(url_for('inv'))


@app.route('/sales_view/<inv_id>', methods=['GET', 'POST'])
def sales_view(inv_id):
    case_inv = InventoryModel.query.filter_by(id=inv_id).first()
    case_sale = SalesModel.query.filter_by(inv_id=inv_id).all()
    if case_sale:
        return render_template('inv_subtemplates/inv_sales.html', sls=case_sale, inv=case_inv)
    elif len(case_sale) == 0:
        flash('Sorry, no sales have been made for {} - {}'.format(case_inv.invname, case_inv.invtype), 'warning')
        return redirect(url_for('inv'))
    else:
        flash("Sorry, don't know what is going on", 'danger')
        return redirect(url_for('inv'))


@app.route('/del-inv', methods=['GET', 'POST'])
def del_inv():
    if request.method == 'POST':
        inv_id = request.form['inventory_id']
        delete_option = request.form['delete']
        case_inv = InventoryModel.query.filter_by(id=inv_id).first()

        if case_inv and delete_option == "Yes":
            db.session.delete(case_inv)
            db.session.commit()

        return redirect(url_for('inv'))


@app.route('/tot-sales', methods=['GET', 'POST'])
def total_sales():
    sales_list = SalesModel.query.join(InventoryModel).add_columns(SalesModel.created_at, SalesModel.id,
                                                                   InventoryModel.invname,
                                                                   InventoryModel.invtype, InventoryModel.sp,
                                                                   SalesModel.qty)
    if sales_list:
        sls = sales_list.order_by(SalesModel.created_at)
    else:
        flash("Sorry, don't know what is going on", 'danger')

    return render_template('tot-sales.html', sls=sls)


if __name__ == '__main__':
    app.run()
