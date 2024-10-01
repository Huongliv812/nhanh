import requests

def get_contact_list(nhanh_token, appId, businessId, page=None, icpp=None):
    url = 'https://open.nhanh.vn/api/customer/search'
    
    # Dữ liệu gửi đi dưới dạng form
    data = {
        "version": "2.0",
        "appId": appId,
        "businessId": businessId,
        "accessToken": nhanh_token
    }

    # Chỉ thêm page và icpp nếu chúng có giá trị
    query_data = {}
    if page:
        query_data["page"] = page
    if icpp:
        query_data["icpp"] = icpp

    # Chuyển đổi query_data thành chuỗi JSON và thêm vào 'data'
    if query_data:
        data["data"] = str(query_data).replace("'", '"')

    response = requests.post(url, data=data)

    # Kiểm tra kết quả
    if response.status_code == 200:
        print("Customer list retrieved successfully.")
        return response.json()  # Trả về JSON chứa danh sách khách hàng
    else:
        print(f"Failed to retrieve customers. Status code: {response.status_code}")
        return None
