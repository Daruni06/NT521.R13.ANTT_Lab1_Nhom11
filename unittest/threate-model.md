## (a) Actor / Role
| Role | Mục đích gọi hàm |
|---|---|
| admin | Quản trị hạ tầng, cần đọc mọi trường kể cả apiKey |
| operator | Vận hành mạng, cần managementIpAddress và issueSummary |
| viewer | Chỉ xem tóm tắt sự cố (issueSummary) |

## (b) Asset nhạy cảm
- apiKey (chuỗi SNMP community): nhạy cảm nhất, chỉ admin
- managementIpAddress: thông tin định danh thiết bị, admin và operator
- Khác: macAddress, serialNumber, lineCardId, cisco360view

## (c) Trust boundary bị bỏ qua
Nếu hàm không kiểm tra role, ranh giới giữa "người gọi có quyền thấp"
và "dữ liệu thô từ API DNAC chứa secret" bị xoá bỏ: hàm trả thẳng
dữ liệu cho mọi người gọi.

## (d) Phân tích STRIDE
| Loại | Threat | Ví dụ |
|---|---|---|
| Information Disclosure | Viewer đọc apiKey | json_search("apiKey", data, role="viewer") |
| Information Disclosure | Lộ secret qua khoá cha | json_search("deviceDetails", data, role="viewer") trả cả dict chứa apiKey |
| Elevation of Privilege | Bỏ qua role hoặc dùng role lạ để đọc | role=None, role="hacker" |
| Spoofing | Người gọi tự khai role | Ngoài phạm vi hàm, cần xác thực ở tầng trên |
| Repudiation | Không ghi log ai đọc trường nhạy cảm | Đề xuất audit log |
| Denial of Service | JSON lồng quá sâu gây RecursionError | Giới hạn độ sâu |
