from flask import Flask, request, render_template, redirect, url_for
from api.getOrderList import get_order_list
from api.getContactList import get_contact_list
from baseopensdk import BaseClient
from function.order_process import process_order
from function.customer_process import process_customer

# Chỉ định thư mục chứa template là 'view'
app = Flask(__name__, template_folder='view')

# Trang chọn loại đồng bộ
@app.route('/', methods=['GET', 'POST'])
def choose_type():
    if request.method == 'POST':
        api_type = request.form['api_type']
        if api_type == 'get_order':
            return redirect(url_for('order_form'))
        elif api_type == 'get_customer':
            return redirect(url_for('contact_form'))
    return render_template('choose_type.html')

# Form để đồng bộ customer
@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        APP_TOKEN = request.form.get('APP_TOKEN')
        PERSONAL_BASE_TOKEN = request.form.get('PERSONAL_BASE_TOKEN')
        TABLE_ID = request.form.get('TABLE_ID')
        NHANH_TOKEN = request.form.get('NHANH_TOKEN')
        APP_ID = request.form.get('APP_ID')
        BUSINESS_ID = request.form.get('BUSINESS_ID')

        # Kiểm tra nếu thiếu APP_TOKEN hoặc PERSONAL_BASE_TOKEN
        if not APP_TOKEN or not PERSONAL_BASE_TOKEN:
            return "APP_TOKEN và PERSONAL_BASE_TOKEN không được bỏ trống.", 400

        # Lấy page, nếu không có thì mặc định là None
        page = request.form.get('page')
        if page:
            try:
                page = int(page)
            except ValueError:
                return "Invalid page number.", 400

        # Gọi API Nhanh.vn để lấy danh sách customer
        customer_data = get_contact_list(
            nhanh_token=NHANH_TOKEN,
            appId=APP_ID,
            businessId=BUSINESS_ID,
            page=page
        )

        if customer_data:
            # Gửi dữ liệu vào Base
            try:
                client = BaseClient.builder().app_token(APP_TOKEN).personal_base_token(PERSONAL_BASE_TOKEN).build()
                process_customer(client, TABLE_ID, customer_data)
                return "Customer data successfully synced to Base."
            except Exception as e:
                print(f"Error processing customer: {e}")
                return "Failed to sync customer data.", 500
        else:
            return "Failed to retrieve customer data.", 400

    return render_template('contact_form.html')

# Form để đồng bộ order
@app.route('/order_form', methods=['GET', 'POST'])
def order_form():
    if request.method == 'POST':
        APP_TOKEN = request.form.get('APP_TOKEN')
        PERSONAL_BASE_TOKEN = request.form.get('PERSONAL_BASE_TOKEN')
        TABLE_ID = request.form.get('TABLE_ID')
        NHANH_TOKEN = request.form.get('NHANH_TOKEN')
        APP_ID = request.form.get('APP_ID')
        BUSINESS_ID = request.form.get('BUSINESS_ID')

        # Kiểm tra nếu thiếu APP_TOKEN hoặc PERSONAL_BASE_TOKEN
        if not APP_TOKEN or not PERSONAL_BASE_TOKEN:
            return "APP_TOKEN và PERSONAL_BASE_TOKEN không được bỏ trống.", 400

        # Lấy fromDate, toDate và page, có thể là None
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate')
        page = request.form.get('page')
        if page:
            try:
                page = int(page)
            except ValueError:
                return "Invalid page number.", 400

        # Gọi API Nhanh.vn để lấy danh sách order
        order_data = get_order_list(
            nhanh_token=NHANH_TOKEN,
            appId=APP_ID,
            businessId=BUSINESS_ID,
            fromDate=fromDate,
            toDate=toDate,
            page=page
        )

        if order_data:
            # Gửi dữ liệu vào Base
            try:
                client = BaseClient.builder().app_token(APP_TOKEN).personal_base_token(PERSONAL_BASE_TOKEN).build()
                process_order(client, TABLE_ID, order_data)
                return "Order data successfully synced to Base."
            except Exception as e:
                print(f"Error processing order: {e}")
                return "Failed to sync order data.", 500
        else:
            return "Failed to retrieve order data.", 400

    return render_template('order_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
