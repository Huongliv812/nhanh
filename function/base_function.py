import pandas as pd
from baseopensdk.api.base.v1 import *

def get_bitable_fields(client, table_id):
    try:
        request = ListAppTableFieldRequest.builder() \
            .table_id(table_id) \
            .build()
        response = client.base.v1.app_table_field.list(request)
        if response.code == 0:
            fields = response.data.items
            field_names = {field.field_name: field for field in fields}
            return field_names
        else:
            print(f"Failed to get Bitable fields. Error: {response.msg}")
            return {}
    except Exception as e:
        print(f"Error getting Bitable fields: {e}")
        return {}

def create_bitable_field(client, table_id, field_name, field_type=1):
    try:
        request = CreateAppTableFieldRequest.builder() \
            .table_id(table_id) \
            .request_body(AppTableField.builder()
                          .field_name(field_name)
                          .type(field_type)
                          .build()) \
            .build()

        response = client.base.v1.app_table_field.create(request)
        if response.code == 0:
            print(f"Field '{field_name}' created successfully.")
            return response.data.field
        else:
            print(f"Failed to create field '{field_name}'. Error: {response.msg}")
            return None
    except Exception as e:
        print(f"Error creating field '{field_name}': {e}")
        return None

def create_bitable_record(client, table_id, row, df_columns, bitable_fields):
    fields = {}
    for col in df_columns:
        value = row.get(col)

        if pd.notnull(value):
            bitable_field = bitable_fields.get(col)
            if bitable_field is None:
                print(f"Warning: Field '{col}' does not exist in Bitable fields. Skipping...")
                continue

            try:
                fields[bitable_field.field_id] = str(value)
            except Exception as e:
                print(f"Error converting field '{col}' with value '{value}'. Error: {e}")
                continue

    try:
        request = CreateAppTableRecordRequest.builder() \
            .table_id(table_id) \
            .request_body(AppTableRecord.builder()
                          .fields(fields)
                          .build()) \
            .build()

        response = client.base.v1.app_table_record.create(request)
        if response.code == 0:
            print(f"Record added successfully for order {row['order_id']}.")
        else:
            print(f"Failed to add record for order {row['order_id']}. Error: {response.msg}")
    except Exception as e:
        print(f"Error creating record for order. Error: {e}")