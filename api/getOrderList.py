import requests

def get_order_list(haravan_token, status=None, created_at_min=None, created_at_max=None, limit=None, page=None, order=None):
    url = 'https://apis.haravan.com/com/orders.json'
    
    headers = {
        'Authorization': f'Bearer {haravan_token}',
        'Content-Type': 'application/json'
    }

    # Tham số truy vấn
    params = {}

    if status:
        params['status'] = status
    if created_at_min:
        params['created_at_min'] = created_at_min
    if created_at_max:
        params['created_at_max'] = created_at_max
    if limit:
        params['limit'] = limit
    if page:
        params['page'] = page
    if order:
        params['order'] = order

    # Gọi API
    response = requests.get(url, headers=headers, params=params)

    # Kiểm tra response
    if response.status_code == 200:
        print("Order list retrieved successfully.")
        return response.json()  # Trả về JSON chứa danh sách đơn hàng
    else:
        print(f"Failed to retrieve orders. Status code: {response.status_code}")
        return None
