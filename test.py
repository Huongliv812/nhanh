# Ví dụ test hàm get_contact_list
from api.getContactList import get_contact_list

nhanh_token = "RWZJYXLJRTgJOs7k1L0QByO2LWhiR2Cxt5nuI2JidzEVahmiGoAQ0nvBWsGIQKKxBvn2gb1T1ZWWnmedjtlT2ksLglGp70nGihPbMszQjreqmsBpN7VFeL7sLGPvNNx72sO9a5Yh7u47gX262h4ktwaCoiu1ViJXwD7yovbvU4ceAwGgonOvjYYIjzvn7DrtL11FRlxD7RVba0JO5jxNUxyc7RBIwYqzaEwj98nAKRso"
appId = "74642"
businessId = "51905"

# Không truyền page và icpp (có thể null)
result = get_contact_list(nhanh_token, appId, businessId)

if result:
    print(result)
else:
    print("Failed to retrieve data.")
