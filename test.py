from baseopensdk import BaseClient
from baseopensdk.api.base.v1 import *
from function.base_function import get_bitable_fields, create_bitable_record

def test_add_order_record():
    # Giả lập thông tin kết nối và bảng
    APP_TOKEN = "EHVfbNry1a81WusjwX2lsCa3gyb"  # Thay bằng App Token của bạn
    PERSONAL_BASE_TOKEN = "pt-hYncnlcOR-K5XDLuooOTNvFi69hfFPh4Zkua4maRAQAAIMAA2h8AgZApcS7l"  # Thay bằng Personal Base Token của bạn
    TABLE_ID = "tblpC1O8fpoBfbHy"  # Thay bằng Table ID của bảng trong Bitable

    # Khởi tạo client Base
    client = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    # Lấy danh sách các trường hiện có trong bảng Bitable
    bitable_fields = get_bitable_fields(client, TABLE_ID)
    if not bitable_fields:
        print("Failed to get Bitable fields. Exiting.")
        return

    # Giả lập dữ liệu order
    fake_order_data = {
        "text": "1234567890"
    }

    # Danh sách các cột trong dữ liệu
    df_columns = list(fake_order_data.keys())

    # Thêm bản ghi vào bảng Bitable
    create_bitable_record(client, TABLE_ID, fake_order_data, df_columns, bitable_fields)

if __name__ == "__main__":
    test_add_order_record()
