import requests
from function.order_process import process_order
from function.customer_process import process_customer
from function.base_function import create_bitable_record, get_bitable_fields


def sync_orders(client, haravan_token, table_id):
    url = 'https://apis.haravan.com/com/orders.json'
    headers = {
        'Authorization': f'Bearer {haravan_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        orders = data.get("orders", [])
        if orders:
            bitable_fields = get_bitable_fields(client, table_id)

            for order in orders:
                records = process_order(order)
                for record in records:
                    create_bitable_record(client, table_id, record, record.keys(), bitable_fields)
            return "Orders processed successfully."
        else:
            return "No orders found."
    else:
        return f"Failed to fetch orders. Status code: {response.status_code}"


def sync_customers(client, haravan_token, table_id):
    url = 'https://apis.haravan.com/com/customers.json'
    headers = {
        'Authorization': f'Bearer {haravan_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        customers = data.get("customers", [])
        if customers:
            bitable_fields = get_bitable_fields(client, table_id)

            for customer in customers:
                records = process_customer(customer)
                for record in records:
                    create_bitable_record(client, table_id, record, record.keys(), bitable_fields)
            return "Customers processed successfully."
        else:
            return "No customers found."
    else:
        return f"Failed to fetch customers. Status code: {response.status_code}"
