from django.apps import AppConfig

"""
Cấu hình ứng dụng `attendance` trong Django.

Đoạn mã này định nghĩa một lớp `AttendanceConfig` kế thừa từ `AppConfig` của Django. Lớp này cung cấp các cấu hình cho ứng dụng `attendance`.

Các thuộc tính:
- `default_auto_field`: Xác định kiểu trường tự động cho các trường khóa chính mặc định của mô hình. Trong trường hợp này, kiểu trường tự động được đặt là `django.db.models.BigAutoField`.
- `name`: Xác định tên của ứng dụng. Trong trường hợp này, tên ứng dụng được đặt là `'attendance'`.

"""

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
