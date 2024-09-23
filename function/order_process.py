from function.base_function import create_bitable_record, create_bitable_field, get_bitable_fields

def process_order(client, table_id, order_data):
    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)
    if not bitable_fields:
        print("Could not retrieve Bitable fields. Exiting.")
        return

    processed_data = []

    # Duyệt qua từng đơn hàng trong order_data
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

        # Xử lý từng mặt hàng trong đơn hàng
        for item in order.get('line_items', []):
            product_name = item.get('title', 'Unknown')
            product_quantity = item.get('quantity', 1)
            product_price = item.get('price', 0)

            # Tạo bản ghi từ dữ liệu
            record = {
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
            }
            processed_data.append(record)

            # Lấy danh sách tên cột từ bản ghi
            df_columns = list(record.keys())

            # Kiểm tra và tạo fields trong Bitable nếu chúng chưa tồn tại
            for df_col in df_columns:
                if df_col not in bitable_fields:
                    # Tạo field trong Bitable
                    new_field = create_bitable_field(client, table_id, df_col)
                    if new_field:
                        bitable_fields[df_col] = new_field
                else:
                    print(f"Field '{df_col}' already exists in Bitable.")

            # Chèn dữ liệu vào Bitable
            create_bitable_record(client, table_id, record, df_columns, bitable_fields)

    print(f"Processed {len(processed_data)} records.")
