from function.base_function import create_bitable_record, create_bitable_field, get_bitable_fields

def process_customer(client, table_id, customer_data):
    # Danh sách các trường cần thiết
    required_fields = ['customer_id', 'customer_name', 'customer_phone', 'customer_email', 
                       'orders_count', 'total_spent', 'state', 'created_at', 'updated_at', 
                       'last_order_id', 'last_order_name', 'last_order_date', 'address_id', 
                       'address1', 'address2', 'city', 'province', 'district', 'ward', 
                       'zipcode', 'phone', 'default']

    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)
    
    # Kiểm tra và chỉ tạo những trường cần thiết nếu chúng chưa tồn tại
    for field in required_fields:
        if field not in bitable_fields:
            new_field = create_bitable_field(client, table_id, field)
            if new_field:
                bitable_fields[field] = new_field

    # Xử lý từng khách hàng
    for customer in customer_data.get('customers', []):
        customer_info = {
            "customer_id": customer.get("id"),
            "customer_name": f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip(),
            "customer_phone": customer.get("phone", ""),
            "customer_email": customer.get("email", ""),
            "orders_count": customer.get("orders_count", 0),
            "total_spent": customer.get("total_spent", 0.0),
            "state": customer.get("state", ""),
            "created_at": customer.get("created_at", ""),
            "updated_at": customer.get("updated_at", ""),
            "last_order_id": customer.get("last_order_id"),
            "last_order_name": customer.get("last_order_name"),
            "last_order_date": customer.get("last_order_date")
        }

        records = []
        addresses = customer.get("addresses", [])
        for address in addresses:
            record = customer_info.copy()  # Sao chép dữ liệu chung của khách hàng
            record.update({
                "address_id": address.get("id"),
                "address1": address.get("address1", ""),
                "address2": address.get("address2", ""),
                "city": address.get("city", ""),
                "province": address.get("province", ""),
                "district": address.get("district", ""),
                "ward": address.get("ward", ""),
                "zipcode": address.get("zip", ""),
                "phone": address.get("phone", ""),  # Thêm field "phone"
                "default": address.get("default", False)  # Thêm field "default"
            })
            records.append(record)

        # Chèn dữ liệu vào Bitable cho mỗi địa chỉ của khách hàng
        for record in records:
            create_bitable_record(client, table_id, record, list(record.keys()), bitable_fields)
