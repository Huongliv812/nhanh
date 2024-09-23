from function.base_function import create_bitable_record, create_bitable_field, get_bitable_fields

def process_customer(client, table_id, customer_data):
    # Lấy danh sách các fields hiện có trong Bitable
    bitable_fields = get_bitable_fields(client, table_id)
    if not bitable_fields:
        print("Could not retrieve Bitable fields. Exiting.")
        return

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
            record = customer_info.copy()
            record.update({
                "address_id": address.get("id"),
                "address1": address.get("address1", ""),
                "address2": address.get("address2", ""),
                "city": address.get("city", ""),
                "province": address.get("province", ""),
                "district": address.get("district", ""),
                "ward": address.get("ward", ""),
                "zipcode": address.get("zip", ""),
                "phone": address.get("phone", ""),
                "default": address.get("default", False)
            })
            records.append(record)

        # Lấy danh sách các cột từ records
        df_columns = list(records[0].keys()) if records else []

        # Kiểm tra và tạo fields trong Bitable nếu chúng chưa tồn tại
        for df_col in df_columns:
            if df_col not in bitable_fields:
                new_field = create_bitable_field(client, table_id, df_col)
                if new_field:
                    bitable_fields[df_col] = new_field
            else:
                print(f"Field '{df_col}' already exists in Bitable.")

        # Chèn dữ liệu vào Bitable
        for record in records:
            create_bitable_record(client, table_id, record, df_columns, bitable_fields)
