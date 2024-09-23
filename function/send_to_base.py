from function.base_function import create_bitable_record, get_bitable_fields

def send_to_base(client, table_id, records):
    # Lấy danh sách các fields hiện có trên Base
    bitable_fields = get_bitable_fields(client, table_id)

    # Lặp qua từng bản ghi và gửi vào Base
    for record in records:
        create_bitable_record(client, table_id, record, list(record.keys()), bitable_fields)
        print(f"Record sent to Base: {record}")
    
    print(f"{len(records)} records sent to Base.")
