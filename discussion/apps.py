from django.apps import AppConfig

class DiscussionConfig(AppConfig):
    """
    Cấu hình ứng dụng Discussion.

    Attributes:
        default_auto_field (str): Tên của trường tự động tạo khóa chính (primary key) trong model.
        name (str): Tên của ứng dụng.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'discussion'