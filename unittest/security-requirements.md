# Security Requirements: json_search()

- SR-1: Hệ thống chỉ trả về giá trị của trường X cho các role nằm trong
  POLICY[X] (policy.py).
- SR-2: role=None hoặc role không hợp lệ không được đọc bất kỳ trường
  nào có trong POLICY (fail-closed).
- SR-3: Kết quả trả về của khoá cha không được chứa các trường con mà
  role không có quyền đọc.
- SR-4 (mở rộng): Xử lý dữ liệu lồng sâu không gây crash.
