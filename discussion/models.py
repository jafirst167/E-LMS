from django.db import models
from main.models import Student, Faculty, Course


class StudentDiscussion(models.Model):
    """
    Model để lưu trữ thông tin về cuộc thảo luận của sinh viên.

    Attributes:
        content (TextField): Nội dung của cuộc thảo luận.
        course (ForeignKey): Liên kết với model Course thông qua khóa ngoại.
        sent_by (ForeignKey): Liên kết với model Student thông qua khóa ngoại.
        sent_at (DateTimeField): Thời điểm gửi cuộc thảo luận.
    """
    content = models.TextField(max_length=1600, null=False)
    course = models.ForeignKey(
        Course, on_delete = models.CASCADE, related_name = 'discussions')
    sent_by = models.ForeignKey(
        Student, on_delete = models.CASCADE, related_name = 'discussions')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Lớp Meta của model StudentDiscussion.

        Attributes:
            ordering (list): Sắp xếp các cuộc thảo luận theo thời gian gửi (giảm dần).
        """
        ordering = ['-sent_at']

    def __str__(self):
        """
        Phương thức string của model StudentDiscussion.

        Returns:
            str: Nội dung cuộc thảo luận (tối đa 30 ký tự).
        """
        return self.content[:30]

    def time(self):
        """
        Phương thức trả về thời điểm gửi cuộc thảo luận dưới dạng chuỗi.

        Returns:
            str: Chuỗi thời điểm gửi cuộc thảo luận (định dạng "%d-%b-%y, %I:%M %p").
        """
        return self.sent_at.strftime("%d-%b-%y, %I:%M %p")


class FacultyDiscussion(models.Model):
    """
    Model để lưu trữ thông tin về cuộc thảo luận của giảng viên.

    Attributes:
        content (TextField): Nội dung của cuộc thảo luận.
        course (ForeignKey): Liên kết với model Course thông qua khóa ngoại.
        sent_by (ForeignKey): Liên kết với model Faculty thông qua khóa ngoại.
        sent_at (DateTimeField): Thời điểm gửi cuộc thảo luận.
    """
    content = models.TextField(max_length = 1600, null = False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name = 'courseDiscussions')
    sent_by = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name = 'courseDiscussions')
    sent_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        """
        Lớp Meta của model FacultyDiscussion.

        Attributes:
            ordering (list): Sắp xếp các cuộc thảo luận theo thời gian gửi (giảm dần).
        """
        ordering = ['-sent_at']

    def __str__(self):
        """
        Phương thức string của model FacultyDiscussion.

        Returns:
            str: Nội dung cuộc thảo luận (tối đa 30 ký tự).
        """
        return self.content[:30]

    def time(self):
        """
        Phương thức trả về thời điểm gửi cuộc thảo luận dưới dạng chuỗi.

        Returns:
            str: Chuỗi thời điểm gửi cuộc thảo luận (định dạng "%d-%b-%y, %I:%M %p").
        """
        return self.sent_at.strftime("%d-%b-%y, %I:%M %p")
