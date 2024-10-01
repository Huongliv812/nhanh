from function.base_function import create_bitable_field, get_bitable_fields, create_bitable_record

def process_order(client, table_id, order_data):
    # Danh sách các trường cần thiết
    required_fields = ['order_id', 'customer_name', 'customer_email', 'customer_address', 
                       'customer_city', 'customer_district', 'customer_ward', 
                       'calcTotalMoney', 'statusName', 'products']

    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)

    # Kiểm tra và tạo các trường cần thiết nếu chưa tồn tại
    for field in required_fields:
        if field not in bitable_fields:
            new_field = create_bitable_field(client, table_id, field)
            if new_field:
                bitable_fields[field] = new_field

    processed_data = []

    # Duyệt qua từng đơn hàng
    for order_id, order in order_data['data']['orders'].items():
        customer_name = order.get('customerName', 'Unknown')
        customer_email = order.get('customerEmail', 'Unknown')
        customer_address = order.get('customerAddress', 'Unknown')
        customer_city = order.get('customerCity', 'Unknown')
        customer_district = order.get('customerDistrict', 'Unknown')
        customer_ward = order.get('customerWard', 'Unknown')
        calcTotalMoney = order.get('calcTotalMoney', 0)
        statusName = order.get('statusName', 'Unknown')

        # Duyệt qua từng sản phẩm trong đơn hàng
        for product in order.get('products', []):
            product_name = product.get('productName', 'Unknown')
            product_quantity = product.get('quantity', 0)
            product_price = product.get('price', 0)

            processed_data.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_address': customer_address,
                'customer_city': customer_city,
                'customer_district': customer_district,
                'customer_ward': customer_ward,
                'calcTotalMoney': calcTotalMoney,
                'statusName': statusName,
                'product_name': product_name,
                'product_quantity': product_quantity,
                'product_price': product_price
            })

    # Chèn dữ liệu vào Bitable
    for record in processed_data:
        create_bitable_record(client, table_id, record, list(record.keys()), bitable_fields)
