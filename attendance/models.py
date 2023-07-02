from django.db import models
from main.models import Student, Course

# Create your models here.


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    date = models.DateField(null = False, blank = False)
    status = models.BooleanField(default = False, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        """
        Trả về một chuỗi biểu diễn của đối tượng Attendance.

        Chuỗi bao gồm tên của học sinh, tên khóa học và ngày trong định dạng 'dd-mm-yyyy'.
        """
        return self.student.name + ' - ' + self.course.name + ' - ' + self.date.strftime('%d-%m-%Y')

    def total_absent(self):
        """
        Tính toán và trả về tổng số lần học sinh vắng mặt.

        Hàm đếm số đối tượng Attendance cho học sinh mà trạng thái là False.
        Nếu số lượng là 0, trả về 0. Ngược lại, trừ đi 1 từ số lượng và trả về kết quả.
        """
        attendance = Attendance.objects.filter(student = self.student, status = False).count()
        if attendance == 0:
            return attendance
        else:
            return attendance - 1

    def total_present(self):
        """
        Tính toán và trả về tổng số lần học sinh có mặt.

        Hàm đếm số đối tượng Attendance cho học sinh mà trạng thái là True.
        Nếu số lượng là 0, trả về 0. Ngược lại, trừ đi 1 từ số lượng và trả về kết quả.
        """
        present = Attendance.objects.filter(student = self.student, status = True).count()
        if present == 0:
            return present
        else:
            return present - 1
