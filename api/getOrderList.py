import requests

def get_order_list(nhanh_token, appId, businessId, fromDate=None, toDate=None, page=None):
    url = 'https://open.nhanh.vn/api/order/index'
    
    # Dữ liệu gửi đi dưới dạng form
    data = {
        "version": "2.0",
        "appId": appId,
        "businessId": businessId,
        "accessToken": nhanh_token
    }

    # Chỉ thêm fromDate, toDate và page nếu chúng có giá trị
    if fromDate:
        data["fromDate"] = fromDate
    if toDate:
        data["toDate"] = toDate
    if page:
        data["page"] = page

    response = requests.post(url, data=data)

    # Kiểm tra kết quả
    if response.status_code == 200:
        print("Order list retrieved successfully.")
        return response.json()  # Trả về JSON chứa danh sách đơn hàng
    else:
        print(f"Failed to retrieve orders. Status code: {response.status_code}")
        return None
