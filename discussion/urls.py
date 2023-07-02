from django.urls import path
from . import views

"""
Định nghĩa các URL cho ứng dụng.

urlpatterns: Danh sách các đường dẫn URL của ứng dụng.
- Đường dẫn 'discussion/<int:code>': Trang thảo luận với mã code nguyên dương. Được xử lý bởi hàm views.discussion. Tên đường dẫn là 'discussion'.
- Đường dẫn 'send/<int:code>/<int:std_id>': Trang gửi tin nhắn với mã code và ID sinh viên (cả hai là số nguyên dương). Được xử lý bởi hàm views.send. Tên đường dẫn là 'send'.
- Đường dẫn 'message/<int:code>/<int:fac_id>': Trang gửi tin nhắn với mã code và ID giảng viên (cả hai là số nguyên dương). Được xử lý bởi hàm views.send_fac. Tên đường dẫn là 'send_fac'.
"""

urlpatterns = [
    path('discussion/<int:code>', views.discussion, name = 'discussion'),
    path('send/<int:code>/<int:std_id>', views.send, name = 'send'),
    path('message/<int:code>/<int:fac_id>', views.send_fac, name = 'send_fac'),
]