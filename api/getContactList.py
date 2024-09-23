import requests

def get_contact_list(haravan_token, created_at_min=None, created_at_max=None, limit=None):
    url = 'https://apis.haravan.com/com/customers.json'
    
    headers = {
        'Authorization': f'Bearer {haravan_token}',
        'Content-Type': 'application/json'
    }

    # Tham số truy vấn
    params = {}

    if created_at_min:
        params['created_at_min'] = created_at_min
    if created_at_max:
        params['created_at_max'] = created_at_max
    if limit:
        params['limit'] = limit

    # Gọi API
    response = requests.get(url, headers=headers, params=params)

    # Kiểm tra response
    if response.status_code == 200:
        print("Customer list retrieved successfully.")
        return response.json()  # Trả về JSON chứa danh sách khách hàng
    else:
        print(f"Failed to retrieve customers. Status code: {response.status_code}")
        return None
