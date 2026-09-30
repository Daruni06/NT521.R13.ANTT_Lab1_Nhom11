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
## (d) Phân tích STRIDE

| Loại | Threat | Kịch bản | Biện pháp |
|---|---|---|---|---|
| **S**poofing | Người gọi khai role giả (ví dụ tự gán role="admin") để đọc secret | Viewer gọi json_search("apiKey", data, role="admin") | Role phải do tầng xác thực bên ngoài cấp, hàm chỉ tin role đã được xác thực |
| **T**ampering | Người gọi sửa dữ liệu gốc hoặc POLICY thông qua kết quả trả về | Sửa dict trả về làm thay đổi `data`; hoặc sửa `POLICY` lúc runtime để tự cấp quyền | Trả về bản sao (copy) chứ không trả tham chiếu tới dữ liệu gốc; coi POLICY là hằng, không cho ghi |
| **R**epudiation | Không có dấu vết ai đã đọc trường nhạy cảm | Admin đọc apiKey, sau này không truy được ai đã đọc | Ghi audit log (role, key, thời điểm, có bị từ chối không) |
| **I**nformation Disclosure | Viewer đọc apiKey | json_search("apiKey", data, role="viewer") | Kiểm tra POLICY trước khi trả |
| **I**nformation Disclosure | Lộ secret qua khoá cha | json_search("deviceDetails", data, role="viewer") trả cả dict chứa apiKey | Lọc trường con bị cấm (redact) |
| **D**enial of Service | JSON lồng quá sâu gây RecursionError, hoặc dữ liệu quá lớn | Dữ liệu lồng vài nghìn tầng làm hàm crash | Giới hạn độ sâu đệ quy |
| **E**levation of Privilege | Bỏ qua role hoặc dùng role lạ để đọc trường bị hạn chế | role=None, role="hacker" | Fail-closed: role không hợp lệ bị từ chối |
