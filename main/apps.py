from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Cấu hình trường khóa tự động mặc định
    name = 'main'  # Tên ứng dụng