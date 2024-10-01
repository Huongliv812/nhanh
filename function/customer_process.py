from function.base_function import create_bitable_field, get_bitable_fields, create_bitable_record

def process_customer(client, table_id, customer_data):
    # Danh sách các trường cần thiết
    required_fields = ['customer_id', 'name', 'mobile', 'email', 'address', 'cityLocationId',
                       'districtLocationId', 'wardLocationId', 'totalMoney', 'startedDate', 
                       'points', 'totalBills', 'lastBoughtDate']

    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)
    
    # Kiểm tra và chỉ tạo những trường cần thiết nếu chúng chưa tồn tại
    for field in required_fields:
        if field not in bitable_fields:
            new_field = create_bitable_field(client, table_id, field)
            if new_field:
                bitable_fields[field] = new_field

    processed_data = []

    for customer_id, customer in customer_data.get('data', {}).get('customers', {}).items():
        customer_info = {
            'customer_id': customer_id,
            'name': customer.get('name', 'Unknown'),
            'mobile': customer.get('mobile', 'Unknown'),
            'email': customer.get('email', 'Unknown'),
            'address': customer.get('address', 'Unknown'),
            'cityLocationId': customer.get('cityLocationId', 'Unknown'),
            'districtLocationId': customer.get('districtLocationId', 'Unknown'),
            'wardLocationId': customer.get('wardLocationId', 'Unknown'),
            'totalMoney': customer.get('totalMoney', 0),
            'startedDate': customer.get('startedDate', 'Unknown'),
            'points': customer.get('points', 0),
            'totalBills': customer.get('totalBills', 0),
            'lastBoughtDate': customer.get('lastBoughtDate', 'Unknown')
        }

        processed_data.append(customer_info)

    # Chèn dữ liệu vào Bitable
    for record in processed_data:
        create_bitable_record(client, table_id, record, list(record.keys()), bitable_fields)
