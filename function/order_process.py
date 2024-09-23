from function.base_function import create_bitable_field, get_bitable_fields, create_bitable_record

def process_order(client, table_id, order_data):
    # Danh sách các trường cần thiết
    required_fields = ['order_id', 'order_number', 'customer_name', 'customer_phone',
                       'customer_email', 'address1', 'province', 'district', 'ward',
                       'financial_status', 'fulfillment_status', 'gateway', 'total_price',
                       'product_name', 'product_quantity', 'product_price']

    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)
    
    # Kiểm tra và chỉ tạo những trường cần thiết nếu chúng chưa tồn tại
    for field in required_fields:
        if field not in bitable_fields:
            new_field = create_bitable_field(client, table_id, field)
            if new_field:
                bitable_fields[field] = new_field

    processed_data = []

    for order in order_data.get('orders', []):
        order_id = order['id']
        order_number = order['order_number']
        customer_name = order['shipping_address']['name'] if order.get('shipping_address') else 'Unknown'
        customer_phone = order['shipping_address']['phone'] if order.get('shipping_address') else 'Unknown'
        customer_email = order.get('email', 'N/A')
        total_price = order.get('total_price', 0)
        gateway = order.get('gateway', 'N/A')
        financial_status = order.get('financial_status', 'N/A')
        fulfillment_status = order.get('fulfillment_status', 'N/A')

        shipping_address = order.get('shipping_address', {})
        address1 = shipping_address.get('address1', '')
        province = shipping_address.get('province', '')
        district = shipping_address.get('district', '')
        ward = shipping_address.get('ward', '')

        for item in order.get('line_items', []):
            product_name = item.get('title', 'Unknown')
            product_quantity = item.get('quantity', 1)
            product_price = item.get('price', 0)

            processed_data.append({
                'order_id': order_id,
                'order_number': order_number,
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'customer_email': customer_email,
                'address1': address1,
                'province': province,
                'district': district,
                'ward': ward,
                'financial_status': financial_status,
                'fulfillment_status': fulfillment_status,
                'gateway': gateway,
                'total_price': total_price,
                'product_name': product_name,
                'product_quantity': product_quantity,
                'product_price': product_price
            })

    # Chèn dữ liệu vào Bitable
    for record in processed_data:
        create_bitable_record(client, table_id, record, list(record.keys()), bitable_fields)
