from django.shortcuts import redirect, render
from discussion.models import FacultyDiscussion, StudentDiscussion
from main.models import Student, Faculty, Course
from main.views import is_faculty_authorised, is_student_authorised
from itertools import chain
from .forms import StudentDiscussionForm, FacultyDiscussionForm


# Create your views here.


''' We have two different user models.
    That's why we are filtering the discussions based on the user type and then combining them.'''


def context_list(course):
    """
    Trả về danh sách các cuộc thảo luận liên quan đến khóa học.

    Tham số:
    - course: Đối tượng khóa học.

    Returns:
    - discussions:  Danh sách các cuộc thảo luận liên quan đến khóa học, được sắp xếp theo thứ tự giảm dần của thời gian gửi.
                    Mỗi cuộc thảo luận có thông tin về tác giả (sinh viên hoặc giảng viên) được gán vào thuộc tính "author".

    Raises:
    - Exception: Nếu xảy ra lỗi trong quá trình truy vấn cuộc thảo luận từ cơ sở dữ liệu.
    """

    try:
        studentDis = StudentDiscussion.objects.filter(course = course)
        facultyDis = FacultyDiscussion.objects.filter(course = course)
        discussions = list(chain(studentDis, facultyDis))
        discussions.sort(key=lambda x: x.sent_at, reverse = True)

        for dis in discussions:
            if dis.__class__.__name__ == 'StudentDiscussion':
                dis.author = Student.objects.get(student_id = dis.sent_by_id)
            else:
                dis.author = Faculty.objects.get(faculty_id = dis.sent_by_id)
    except:
        discussions = []

    return discussions


def discussion(request, code):
    """
    Xử lý yêu cầu hiển thị trang thảo luận cho một khóa học.

    Tham số:
    - request: Đối tượng yêu cầu từ client.
    - code: Mã code của khóa học.

    Returns:
    - Nếu sinh viên được ủy quyền cho khóa học, trả về trang thảo luận của khóa học hiển thị thông tin khóa học, sinh viên, danh sách cuộc thảo luận và biểu mẫu thảo luận của sinh viên.
    - Nếu giảng viên được ủy quyền cho khóa học, trả về trang thảo luận của khóa học hiển thị thông tin khóa học, giảng viên, danh sách cuộc thảo luận và biểu mẫu thảo luận của giảng viên.
    - Nếu không có quyền truy cập hoặc không đăng nhập, chuyển hướng đến trang đăng nhập của sinh viên.

    Raises:
    - Course.DoesNotExist: Nếu không tìm thấy khóa học với mã code tương ứng trong cơ sở dữ liệu.
    - Student.DoesNotExist: Nếu không tìm thấy sinh viên với ID tương ứng trong cơ sở dữ liệu.
    - Faculty.DoesNotExist: Nếu không tìm thấy giảng viên với ID tương ứng trong cơ sở dữ liệu.
    """

    if is_student_authorised(request, code):
        course = Course.objects.get(code = code)
        student = Student.objects.get(student_id=request.session['student_id'])
        discussions = context_list(course)
        form = StudentDiscussionForm()
        context = {
            'course': course,
            'student': student,
            'discussions': discussions,
            'form': form,
        }
        return render(request, 'discussion/discussion.html', context)

    elif is_faculty_authorised(request, code):
        course = Course.objects.get(code = code)
        faculty = Faculty.objects.get(faculty_id = request.session['faculty_id'])
        discussions = context_list(course)
        form = FacultyDiscussionForm()
        context = {
            'course': course,
            'faculty': faculty,
            'discussions': discussions,
            'form': form,
        }
        return render(request, 'discussion/discussion.html', context)
    else:
        return redirect('std_login')


def send(request, code, std_id):
    """
    Xử lý yêu cầu gửi thảo luận từ một sinh viên cho một khóa học.

    Tham số:
    - request: Đối tượng yêu cầu từ client.
    - code: Mã code của khóa học.
    - std_id: ID của sinh viên.

    Returns:
    - Nếu sinh viên được ủy quyền cho khóa học và yêu cầu gửi là phương thức POST, hàm lấy nội dung thảo luận từ biểu mẫu, tạo mới cuộc thảo luận trong cơ sở dữ liệu và chuyển hướng đến trang thảo luận của khóa học.
    - Nếu sinh viên được ủy quyền cho khóa học nhưng yêu cầu gửi không phải là phương thức POST, hàm chuyển hướng đến trang thảo luận của khóa học.
    - Nếu không có quyền truy cập, hàm chuyển hướng đến trang đăng nhập của sinh viên.
    - Nếu không tìm thấy sinh viên tương ứng trong cơ sở dữ liệu, hàm chuyển hướng đến trang thảo luận của khóa học.

    Raises:
    - Course.DoesNotExist: Nếu không tìm thấy khóa học với mã code tương ứng trong cơ sở dữ liệu.
    - Student.DoesNotExist: Nếu không tìm thấy sinh viên với ID tương ứng trong cơ sở dữ liệu.
    """

    if is_student_authorised(request, code):
        if request.method == 'POST':
            form = StudentDiscussionForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                course = Course.objects.get(code = code)
                try:
                    student = Student.objects.get(student_id = std_id)
                except:
                    return redirect('discussion', code = code)
                StudentDiscussion.objects.create(
                    content=content, course=course, sent_by = student)
                return redirect('discussion', code = code)
            else:
                return redirect('discussion', code = code)
        else:
            return redirect('discussion', code = code)
    else:
        return render(request, 'std_login.html')


def send_fac(request, code, fac_id):
    """
    Xử lý yêu cầu gửi thảo luận từ một giảng viên cho một khóa học.

    Tham số:
    - request: Đối tượng yêu cầu từ client.
    - code: Mã code của khóa học.
    - fac_id: ID của giảng viên.

    Returns:
    - Nếu giảng viên được ủy quyền cho khóa học và yêu cầu gửi là phương thức POST, hàm lấy nội dung thảo luận từ biểu mẫu, tạo mới cuộc thảo luận trong cơ sở dữ liệu và chuyển hướng đến trang thảo luận của khóa học.
    - Nếu giảng viên được ủy quyền cho khóa học nhưng yêu cầu gửi không phải là phương thức POST, hàm chuyển hướng đến trang thảo luận của khóa học.
    - Nếu không có quyền truy cập, hàm chuyển hướng đến trang đăng nhập của sinh viên.
    - Nếu không tìm thấy giảng viên tương ứng trong cơ sở dữ liệu, hàm chuyển hướng đến trang thảo luận của khóa học.

    Raises:
    - Course.DoesNotExist: Nếu không tìm thấy khóa học với mã code tương ứng trong cơ sở dữ liệu.
    - Faculty.DoesNotExist: Nếu không tìm thấy giảng viên với ID tương ứng trong cơ sở dữ liệu.
    """

    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = FacultyDiscussionForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                course = Course.objects.get(code = code)
                try:
                    faculty = Faculty.objects.get(faculty_id = fac_id)
                except:
                    return redirect('discussion', code = code)
                FacultyDiscussion.objects.create(
                    content=content, course = course, sent_by = faculty)
                return redirect('discussion', code = code)
            else:
                return redirect('discussion', code = code)
        else:
            return redirect('discussion', code = code)
    else:
        return render(request, 'std_login.html')