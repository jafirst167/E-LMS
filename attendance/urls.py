from django.urls import path
from . import views

"""
Định nghĩa các đường dẫn URL cho ứng dụng.

Module này xác định các đường dẫn URL cho các chức năng trong ứng dụng. Mỗi đường dẫn được gắn kết với một hàm xử lý tương ứng trong module `views`.

Các đường dẫn:
- `/attendance/<int:code>`: Đường dẫn để xem danh sách điểm danh với mã học sinh là `code`.
- `/createRecord/<int:code>`: Đường dẫn để tạo bản ghi điểm danh mới cho học sinh với mã là `code`.
- `/submitAttendance/<int:code>`: Đường dẫn để gửi điểm danh cho học sinh với mã là `code`.
- `/loadAttendance/<int:code>`: Đường dẫn để tải danh sách điểm danh cho học sinh với mã là `code`.
"""

urlpatterns = [
    path('attendance/<int:code>', views.attendance, name = 'attendance'),
    path('createRecord/<int:code>', views.createRecord, name = 'createRecord'),
    path('submitAttendance/<int:code>', views.submitAttendance, name = 'submitAttendance'),
    path('loadAttendance/<int:code>', views.loadAttendance, name = 'loadAttendance'),
]