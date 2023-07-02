from django.db import models
from froala_editor.fields import FroalaField
# Create your models here.


class Student(models.Model):
    """
    Mô hình đại diện cho sinh viên.

    Thuộc tính:
        - student_id: Mã sinh viên (primary key).
        - name: Tên sinh viên.
        - email: Địa chỉ email của sinh viên.
        - password: Mật khẩu của sinh viên.
        - role: Vai trò của sinh viên (mặc định là "Student").
        - course: Danh sách các khóa học mà sinh viên đã đăng ký (ManyToMany relationship).
        - photo: Ảnh đại diện của sinh viên (tải lên vào thư mục 'profile_pics', mặc định là 'profile_pics/default_student.png').
        - department: Bộ môn học của sinh viên (ForeignKey relationship).

    Phương thức:
        - delete: Ghi đè phương thức xóa để xóa ảnh đại diện của sinh viên nếu không phải là ảnh mặc định.

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Student.

    """

    student_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100, null = False)
    email = models.EmailField(max_length = 100, null = True, blank = True)
    password = models.CharField(max_length = 255, null = False)
    role = models.CharField(
        default = "Student", max_length = 100, null = False, blank = True)
    course = models.ManyToManyField(
        'Course', related_name = 'students', blank = True)
    photo = models.ImageField(upload_to = 'profile_pics', blank = True, null = False, default = 'profile_pics/default_student.png')
    department = models.ForeignKey(
        'Department', on_delete = models.CASCADE, null = False, blank = False, related_name = 'students')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name


class Faculty(models.Model):
    """
    Mô hình đại diện cho giảng viên.

    Thuộc tính:
        - faculty_id: Mã giảng viên (primary key).
        - name: Tên giảng viên.
        - email: Địa chỉ email của giảng viên.
        - password: Mật khẩu của giảng viên.
        - department: Bộ môn học của giảng viên (ForeignKey relationship).
        - role: Vai trò của giảng viên (mặc định là "Faculty").
        - photo: Ảnh đại diện của giảng viên (tải lên vào thư mục 'profile_pics', mặc định là 'profile_pics/default_faculty.png').

    Phương thức:
        - delete: Ghi đè phương thức xóa để xóa ảnh đại diện của giảng viên nếu không phải là ảnh mặc định.

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Faculty.

    """

    faculty_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100, null = False)
    email = models.EmailField(max_length = 100, null = True, blank = True)
    password = models.CharField(max_length = 255, null = False)
    department = models.ForeignKey(
        'Department', on_delete = models.CASCADE, null = False, related_name = 'faculty')
    role = models.CharField(
        default = "Faculty", max_length = 100, null = False, blank = True)
    photo = models.ImageField(upload_to = 'profile_pics', blank = True, null = False, default = 'profile_pics/default_faculty.png')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_faculty.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Mô hình đại diện cho bộ môn học.

    Thuộc tính:
        - department_id: Mã bộ môn (primary key).
        - name: Tên bộ môn.
        - description: Mô tả về bộ môn (có thể null và trống).

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Department.

    Phương thức:
        - __str__: Phương thức trả về tên của bộ môn.
        - student_count: Phương thức trả về số lượng sinh viên thuộc bộ môn.
        - faculty_count: Phương thức trả về số lượng giảng viên thuộc bộ môn.
        - course_count: Phương thức trả về số lượng khóa học thuộc bộ môn.

    """
    department_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100, null = False)
    description = models.TextField(null = True, blank = True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def faculty_count(self):
        return self.faculty.count()

    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    """
    Mô hình đại diện cho khóa học.

    Thuộc tính:
        - code: Mã khóa học (primary key).
        - name: Tên khóa học.
        - department: Bộ môn học liên quan đến khóa học (ForeignKey).
        - faculty: Giảng viên phụ trách khóa học (ForeignKey, có thể null và trống).
        - studentKey: Khóa chính để liên kết sinh viên với khóa học (unique).
        - facultyKey: Khóa chính để liên kết giảng viên với khóa học (unique).

    Meta:
        unique_together: Tập hợp các trường duy nhất là 'code', 'department', 'name'.
        verbose_name_plural: Tên số nhiều của lớp Course.

    Phương thức:
        - __str__: Phương thức trả về tên của khóa học.

    """

    code = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 255, null = False, unique = True)
    department = models.ForeignKey(
        Department, on_delete = models.CASCADE, null = False, related_name = 'courses')
    faculty = models.ForeignKey(
        Faculty, on_delete = models.SET_NULL, null = True, blank = True)
    studentKey = models.IntegerField(null = False, unique = True)
    facultyKey = models.IntegerField(null = False, unique = True)

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """
    Mô hình đại diện cho thông báo.

    Thuộc tính:
        - course_code: Mã khóa học mà thông báo thuộc về (ForeignKey).
        - datetime: Thời điểm tạo thông báo (auto_now_add).
        - description: Nội dung thông báo (FroalaField).

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Announcement.
        ordering: Sắp xếp các thông báo theo thời gian giảm dần.

    Phương thức:
        - __str__: Phương thức trả về thời điểm thông báo dưới dạng chuỗi.
        - post_date: Phương thức trả về thời điểm thông báo dưới dạng chuỗi.

    """
    course_code = models.ForeignKey(
        Course, on_delete = models.CASCADE, null = False)
    datetime = models.DateTimeField(auto_now_add = True, null = False)
    description = FroalaField()

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")


class Assignment(models.Model):
    """
    Mô hình đại diện cho bài tập.

    Thuộc tính:
        - course_code: Mã khóa học mà bài tập thuộc về (ForeignKey).
        - title: Tiêu đề của bài tập (CharField).
        - description: Mô tả bài tập (TextField).
        - datetime: Thời điểm tạo bài tập (auto_now_add).
        - deadline: Thời hạn nộp bài (DateTimeField).
        - file: Tệp tin đính kèm cho bài tập (FileField).
        - marks: Điểm số cho bài tập (DecimalField).

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Assignment.
        ordering: Sắp xếp các bài tập theo thời gian giảm dần.

    Phương thức:
        - __str__: Phương thức trả về tiêu đề của bài tập.
        - delete: Phương thức ghi đè để xóa tệp tin đính kèm khi xóa bài tập.
        - post_date: Phương thức trả về thời điểm tạo bài tập dưới dạng chuỗi.
        - due_date: Phương thức trả về thời hạn nộp bài dưới dạng chuỗi.

    """
    course_code = models.ForeignKey(Course, on_delete = models.CASCADE, null = False)
    title = models.CharField(max_length = 255, null = False)
    description = models.TextField(null = False)
    datetime = models.DateTimeField(auto_now_add = True, null = False)
    deadline = models.DateTimeField(null = False)
    file = models.FileField(upload_to = 'assignments/', null = True, blank = True)
    marks = models.DecimalField(max_digits = 6, decimal_places = 2, null = False)

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def due_date(self):
        return self.deadline.strftime("%d-%b-%y, %I:%M %p")


class Submission(models.Model):
    """
    Mô hình đại diện cho bài nộp.

    Thuộc tính:
        - assignment: Bài tập mà bài nộp thuộc về (ForeignKey).
        - student: Sinh viên nộp bài (ForeignKey).
        - file: Tệp tin đính kèm của bài nộp (FileField).
        - datetime: Thời điểm nộp bài (auto_now_add).
        - marks: Điểm số cho bài nộp (DecimalField).
        - status: Trạng thái của bài nộp (CharField).

    Phương thức:
        - file_name: Phương thức trả về tên tệp tin của bài nộp.
        - time_difference: Phương thức trả về khoảng thời gian chênh lệch giữa thời hạn nộp và thời điểm nộp.
        - submission_date: Phương thức trả về thời điểm nộp bài dưới dạng chuỗi.
        - delete: Phương thức ghi đè để xóa tệp tin đính kèm khi xóa bài nộp.
        - __str__: Phương thức trả về chuỗi mô tả bài nộp.

    Meta:
        unique_together: Cặp trường 'assignment' và 'student' là duy nhất.
        verbose_name_plural: Tên số nhiều của lớp Submission.
        ordering: Sắp xếp các bài nộp theo thời gian tăng dần.

    """

    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE, null = False)
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null = False)
    file = models.FileField(upload_to = 'submissions/', null = True,)
    datetime = models.DateTimeField(auto_now_add = True, null = False)
    marks = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank = True)
    status = models.CharField(max_length = 100, null = True, blank = True)

    def file_name(self):
        return self.file.name.split('/')[-1]

    def time_difference(self):
        difference = self.assignment.deadline - self.datetime
        days = difference.days
        hours = difference.seconds//3600
        minutes = (difference.seconds//60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " seconds"
                else:
                    return str(minutes) + " minutes " + str(seconds) + " seconds"
            else:
                return str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            return str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

    def submission_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['datetime']


class Material(models.Model):
    """
    Mô hình đại diện cho tài liệu học tập.

    Thuộc tính:
        - course_code: Mã khóa học mà tài liệu thuộc về (ForeignKey).
        - description: Mô tả tài liệu (TextField).
        - datetime: Thời điểm tạo tài liệu (auto_now_add).
        - file: Tệp tin đính kèm của tài liệu (FileField).

    Phương thức:
        - delete: Phương thức ghi đè để xóa tệp tin đính kèm khi xóa tài liệu.
        - post_date: Phương thức trả về thời điểm đăng tải tài liệu dưới dạng chuỗi.
        - __str__: Phương thức trả về chuỗi mô tả tài liệu.

    Meta:
        verbose_name_plural: Tên số nhiều của lớp Material.
        ordering: Sắp xếp các tài liệu theo thời gian tạo giảm dần.

    """

    course_code = models.ForeignKey(Course, on_delete = models.CASCADE, null = False)
    description = models.TextField(max_length = 2000, null = False)
    datetime = models.DateTimeField(auto_now_add = True, null = False)
    file = models.FileField(upload_to = 'materials/', null = True, blank = True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']