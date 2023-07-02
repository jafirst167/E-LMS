"""
Đăng ký mô hình `Attendance` với trang quản trị Django.

Đoạn mã này import mô hình `Attendance` từ mô-đun `models` của module hiện tại và đăng ký nó với trang quản trị Django. Khi đó, mô hình `Attendance` sẽ có thể được truy cập và quản lý thông qua giao diện quản trị Django.

"""
from django.contrib import admin
from .models import Attendance
# Register your models here.
admin.site.register(Attendance)
