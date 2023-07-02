from django.contrib import admin

# Đăng ký các mô hình để quản lý trong trang quản lý Django
from .models import Student, Faculty, Course, Department, Assignment, Announcement

admin.site.register(Student)  # Đăng ký mô hình Student
admin.site.register(Faculty)  # Đăng ký mô hình Faculty
admin.site.register(Course)  # Đăng ký mô hình Course
admin.site.register(Department)  # Đăng ký mô hình Department
admin.site.register(Assignment)  # Đăng ký mô hình Assignment
admin.site.register(Announcement)  # Đăng ký mô hình Announcement

