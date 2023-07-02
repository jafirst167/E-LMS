"""eLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views
from froala_editor import views as froala_views


admin.site.site_header = "eLMS Administration"
admin.site.site_title = "eLMS Administration Portal"
admin.site.index_title = "Welcome to eLMS Administration Portal"


urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),  # Đường dẫn đến trang quản lý Django

    path('student/', views.guestStudent, name = 'guestStudent'),  # Đường dẫn đến trang đăng nhập và đăng ký của sinh viên
    path('teacher/', views.guestFaculty, name = 'guestFaculty'),  # Đường dẫn đến trang đăng nhập và đăng ký của giảng viên

    path('', include('main.urls')),  # Đường dẫn chính của ứng dụng, liên kết với các URL của ứng dụng main
    path('', include('discussion.urls')),  # Đường dẫn đến các URL của ứng dụng discussion
    path('', include('attendance.urls')),  # Đường dẫn đến các URL của ứng dụng attendance
    path('', include('quiz.urls')),  # Đường dẫn đến các URL của ứng dụng quiz

    path('froala_editor/', include('froala_editor.urls')),  # Đường dẫn đến các URL của ứng dụng froala_editor, ứng dụng cung cấp trình soạn thảo văn bản
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # Đường dẫn tĩnh cho các tệp đa phương tiện

