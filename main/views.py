import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Student, Course, Announcement, Assignment, Submission, Material, Faculty, Department
from django.template.defaulttags import register
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from .forms import AnnouncementForm, AssignmentForm, MaterialForm
from django import forms
from django.core import validators
from django import forms

class LoginForm(forms.Form):
    """
    Một form Django để đăng nhập người dùng.

    Form này chứa hai trường: 'id' và 'password' để xác thực người dùng.

    Attributes:
        id (CharField): Trường nhập ID của người dùng.
        password (CharField): Trường nhập mật khẩu của người dùng.
    """
    id = forms.CharField(label = 'ID', max_length = 10, validators=[validators.RegexValidator(r'^\d+$', 'Please enter a valid number.')])
    password = forms.CharField(widget = forms.PasswordInput)


def is_student_authorised(request, code):
    """
    Kiểm tra xem sinh viên đã được ủy quyền cho một khóa học cụ thể hay chưa.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        bool: Trả về True nếu sinh viên được ủy quyền, False nếu không được ủy quyền.

    Raises:
        Course.DoesNotExist: Nếu không tìm thấy khóa học với mã tương ứng.
    """
    course = Course.objects.get(code = code)
    if request.session.get('student_id') and course in Student.objects.get(student_id = request.session['student_id']).course.all():
        return True
    else:
        return False


def is_faculty_authorised(request, code):
    """
    Kiểm tra xem giảng viên đã được ủy quyền cho một khóa học cụ thể hay chưa.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        bool: Trả về True nếu giảng viên được ủy quyền, False nếu không được ủy quyền.
    """
    if request.session.get('faculty_id') and code in Course.objects.filter(faculty_id = request.session['faculty_id']).values_list('code', flat = True):
        return True
    else:
        return False


def std_login(request):
    """
    Xử lý quá trình đăng nhập cho sinh viên và giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None
    """
    error_messages = []

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']

            # Kiểm tra xem có tồn tại sinh viên với mã sinh viên và mật khẩu tương ứng
            if Student.objects.filter(student_id = id, password = password).exists():
                request.session['student_id'] = id
                return redirect('myCourses')
            # Kiểm tra xem có tồn tại giảng viên với mã giảng viên và mật khẩu tương ứng
            elif Faculty.objects.filter(faculty_id = id, password = password).exists():
                request.session['faculty_id'] = id
                return redirect('facultyCourses')
            else:
                error_messages.append('Invalid login credentials.')
        else:
            error_messages.append('Invalid form data.')
    else:
        form = LoginForm()

    # Kiểm tra nếu đã đăng nhập dưới tài khoản sinh viên, chuyển hướng đến trang của sinh viên
    if 'student_id' in request.session:
        return redirect('/my/')
    # Kiểm tra nếu đã đăng nhập dưới tài khoản giảng viên, chuyển hướng đến trang của giảng viên
    elif 'faculty_id' in request.session:
        return redirect('/facultyCourses/')

    # Gửi form và thông báo lỗi (nếu có) đến template login_page.html
    context = {'form': form, 'error_messages': error_messages}
    return render(request, 'login_page.html', context)


# Clears the session on logout
def std_logout(request):
    """
    Xử lý quá trình đăng xuất cho sinh viên và giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None
    """
    request.session.flush()
    return redirect('std_login')


def myCourses(request):
    """
    Hiển thị danh sách các khóa học của sinh viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Nếu sinh viên đã đăng nhập (có session 'student_id'), danh sách các khóa học của sinh viên sẽ được hiển thị.
        - Danh sách các khóa học bao gồm thông tin về khóa học, sinh viên và giảng viên phụ trách.
        - Nếu sinh viên chưa đăng nhập, sẽ chuyển hướng đến trang đăng nhập ('std_login').
        - Nếu xảy ra lỗi, trang 'error.html' sẽ được hiển thị.

    """
    try:
        if request.session.get('student_id'):
            # Lấy thông tin sinh viên từ session
            student = Student.objects.get(student_id = request.session['student_id'])
            # Lấy danh sách các khóa học của sinh viên
            courses = student.course.all()
            # Lấy danh sách giảng viên phụ trách các khóa học
            faculty = student.course.all().values_list('faculty_id', flat = True)

            context = {
                'courses': courses,
                'student': student,
                'faculty': faculty
            }

            return render(request, 'main/myCourses.html', context)
        else:
            # Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
            return redirect('std_login')
    except Exception:
        # Xử lý lỗi và hiển thị trang 'error.html'
        return render(request, 'error.html')


def facultyCourses(request):
    """
    Hiển thị danh sách các khóa học của giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Nếu giảng viên đã đăng nhập (có session 'faculty_id'), danh sách các khóa học của giảng viên sẽ được hiển thị.
        - Danh sách các khóa học bao gồm thông tin về khóa học và số lượng sinh viên tham gia mỗi khóa học.
        - Nếu giảng viên chưa đăng nhập, sẽ chuyển hướng đến trang đăng nhập ('std_login').
        - Nếu xảy ra lỗi, sẽ chuyển hướng đến trang đăng nhập ('std_login').

    """
    try:
        if request.session['faculty_id']:
            # Lấy thông tin giảng viên từ session
            faculty = Faculty.objects.get(faculty_id = request.session['faculty_id'])
            # Lấy danh sách các khóa học do giảng viên phụ trách
            courses = Course.objects.filter(faculty_id = request.session['faculty_id'])
            # Đếm số lượng sinh viên tham gia mỗi khóa học
            studentCount = Course.objects.all().annotate(student_count = Count('students'))

            studentCountDict = {}

            for course in studentCount:
                studentCountDict[course.code] = course.student_count

            @register.filter
            def get_item(dictionary, course_code):
                return dictionary.get(course_code)

            context = {
                'courses': courses,
                'faculty': faculty,
                'studentCount': studentCountDict
            }

            return render(request, 'main/facultyCourses.html', context)

        else:
            # Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
            return redirect('std_login')
    except Exception:
        # Xử lý lỗi và chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def course_page(request, code):
    """
    Hiển thị trang chi tiết khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Nếu sinh viên được ủy quyền (có quyền truy cập vào khóa học), trang chi tiết khóa học sẽ được hiển thị.
        - Trang chi tiết khóa học bao gồm danh sách thông báo, danh sách bài tập và danh sách tài liệu liên quan đến khóa học.
        - Nếu sinh viên chưa đăng nhập hoặc không có quyền truy cập vào khóa học, sẽ chuyển hướng đến trang đăng nhập ('std_login').
        - Nếu xảy ra lỗi, sẽ hiển thị trang lỗi ('error.html').
    """
    try:
        course = Course.objects.get(code = code)
        if is_student_authorised(request, code):
            try:
                # Lấy danh sách thông báo, danh sách bài tập và danh sách tài liệu của khóa học
                announcements = Announcement.objects.filter(course_code = course)
                assignments = Assignment.objects.filter(course_code = course.code)
                materials = Material.objects.filter(course_code = course.code)

            except Exception:
                announcements = None
                assignments = None
                materials = None

            context = {
                'course': course,
                'announcements': announcements,
                'assignments': assignments[:3],
                'materials': materials,
                'student': Student.objects.get(student_id=request.session['student_id'])
            }

            return render(request, 'main/course.html', context)

        else:
            # Nếu không có quyền truy cập, chuyển hướng đến trang đăng nhập
            return redirect('std_login')
    except Exception:
        # Xử lý lỗi và hiển thị trang lỗi
        return render(request, 'error.html')


def course_page_faculty(request, code):
    """
    Hiển thị trang chi tiết khóa học cho giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Nếu giảng viên đã đăng nhập (có session 'faculty_id'), trang chi tiết khóa học sẽ được hiển thị.
        - Trang chi tiết khóa học bao gồm danh sách thông báo, danh sách bài tập, danh sách tài liệu và số lượng sinh viên tham gia khóa học.
        - Nếu giảng viên chưa đăng nhập, hàm sẽ chuyển hướng người dùng đến trang đăng nhập ('std_login').

    """
    course = Course.objects.get(code=code)
    if request.session.get('faculty_id'):
        try:
            # Lấy danh sách thông báo, danh sách bài tập, danh sách tài liệu và số lượng sinh viên tham gia khóa học
            announcements = Announcement.objects.filter(course_code = course)
            assignments = Assignment.objects.filter(course_code = course.code)
            materials = Material.objects.filter(course_code = course.code)
            studentCount = Student.objects.filter(course = course).count()

        except Exception:
            announcements = None
            assignments = None
            materials = None

        context = {
            'course': course,
            'announcements': announcements,
            'assignments': assignments[:3],
            'materials': materials,
            'faculty': Faculty.objects.get(faculty_id = request.session['faculty_id']),
            'studentCount': studentCount
        }

        return render(request, 'main/faculty_course.html', context)
    else:
        # Nếu giảng viên chưa đăng nhập, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def error(request):
    """
    Hiển thị trang lỗi.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Trang lỗi ('error.html') sẽ được hiển thị.

    """
    return render(request, 'error.html')


def profile(request, id):
    """
    Hiển thị trang hồ sơ cá nhân.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        id (str): ID của sinh viên hoặc giảng viên.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Nếu người dùng đăng nhập là sinh viên và ID trùng khớp với ID được cung cấp, trang hồ sơ cá nhân của sinh viên sẽ được hiển thị.
        - Nếu người dùng đăng nhập là giảng viên và ID trùng khớp với ID được cung cấp, trang hồ sơ cá nhân của giảng viên sẽ được hiển thị.
        - Nếu không có người dùng đăng nhập hoặc không có trùng khớp với ID được cung cấp, người dùng sẽ được chuyển hướng đến trang đăng nhập.
        - Trang lỗi ('error.html') sẽ được hiển thị nếu xảy ra lỗi trong quá trình xử lý.

    """
    try:
        if request.session['student_id'] == id:
            student = Student.objects.get(student_id = id)
            return render(request, 'main/profile.html', {'student': student})
        else:
            return redirect('std_login')
    except:
        try:
            if request.session['faculty_id'] == id:
                faculty = Faculty.objects.get(faculty_id = id)
                return render(request, 'main/faculty_profile.html', {'faculty': faculty})
            else:
                return redirect('std_login')
        except:
            return render(request, 'error.html')


def addAnnouncement(request, code):
    """
    Thêm thông báo mới vào khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Yêu cầu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Nếu phương thức yêu cầu là POST, thông báo mới sẽ được thêm vào khóa học sau khi kiểm tra và lưu trữ dữ liệu từ form.
        - Nếu phương thức yêu cầu không phải là POST, form trống sẽ được hiển thị để người dùng nhập thông tin.
        - Sau khi thông báo được thêm thành công, người dùng sẽ được chuyển hướng đến trang khóa học tương ứng.
        - Trang đăng nhập ('std_login') sẽ được chuyển hướng đến nếu người dùng không đủ quyền truy cập.

    """
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            form.instance.course_code = Course.objects.get(code = code)
            if form.is_valid():
                form.save()
                messages.success(request, 'Announcement added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AnnouncementForm()
        return render(request, 'main/announcement.html', {'course': Course.objects.get(code = code), 'faculty': Faculty.objects.get(faculty_id = request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def deleteAnnouncement(request, code, id):
    """
    Xóa thông báo khỏi khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.
        id (int): ID của thông báo.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Yêu cầu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Thông báo có ID tương ứng sẽ được xóa khỏi khóa học.
        - Sau khi thông báo được xóa thành công, người dùng sẽ được chuyển hướng đến trang khóa học tương ứng.
        - Trang đăng nhập ('std_login') sẽ được chuyển hướng đến nếu người dùng không đủ quyền truy cập.

    """
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code = code, id = id)
            announcement.delete()
            messages.warning(request, 'Announcement deleted successfully.')
            return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def editAnnouncement(request, code, id):
    """
    Chỉnh sửa thông báo của khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.
        id (int): ID của thông báo.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Yêu cầu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Thông báo có ID tương ứng sẽ được lấy ra và hiển thị trong form chỉnh sửa thông báo.
        - Trang đăng nhập ('std_login') sẽ được chuyển hướng đến nếu người dùng không đủ quyền truy cập.

    """
    if is_faculty_authorised(request, code):
        announcement = Announcement.objects.get(course_code_id = code, id = id)
        form = AnnouncementForm(instance = announcement)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code = code),
            'faculty': Faculty.objects.get(faculty_id = request.session['faculty_id']),
            'form': form
        }
        return render(request, 'main/update-announcement.html', context)
    else:
        return redirect('std_login')


def updateAnnouncement(request, code, id):
    """
    Cập nhật thông báo của khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.
        id (int): ID của thông báo.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Yêu cầu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Thông báo có ID tương ứng sẽ được lấy ra và cập nhật dựa trên dữ liệu gửi lên từ form.
        - Trang đăng nhập ('std_login') sẽ được chuyển hướng đến nếu người dùng không đủ quyền truy cập.

    """
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code_id = code, id = id)
            form = AnnouncementForm(request.POST, instance = announcement)
            if form.is_valid():
                form.save()
                messages.info(request, 'Announcement updated successfully.')
                return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))

    else:
        return redirect('std_login')


def addAssignment(request, code):
    """
    Thêm bài tập cho khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Yêu cầu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Nếu yêu cầu là phương thức POST, form sẽ được gửi lên và kiểm tra tính hợp lệ.
        - Nếu form hợp lệ, bài tập sẽ được lưu và thông báo thành công sẽ được hiển thị.
        - Trang đăng nhập ('std_login') sẽ được chuyển hướng đến nếu người dùng không đủ quyền truy cập.

    """
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AssignmentForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code = code)
            if form.is_valid():
                form.save()
                messages.success(request, 'Assignment added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AssignmentForm()
        return render(request, 'main/assignment.html', {'course': Course.objects.get(code = code), 'faculty': Faculty.objects.get(faculty_id = request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def assignmentPage(request, code, id):
    """
    Hiển thị trang bài tập.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.
        id (int): ID của bài tập.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Trang bài tập sẽ được hiển thị cho người dùng nếu người dùng là sinh viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Thông tin về bài tập và nộp bài tập (nếu có) sẽ được truy xuất và truyền vào template để hiển thị.
        - Nếu không tìm thấy bài nộp bài tập từ sinh viên, biến `submission` sẽ được gán giá trị `None`.
        - Thời gian hiện tại (`datetime.now()`) cũng sẽ được truyền vào template để thực hiện các tính toán liên quan đến thời gian.

    """
    # Lấy thông tin khóa học
    course = Course.objects.get(code = code)

    # Kiểm tra người dùng có quyền truy cập vào khóa học hay không
    if is_student_authorised(request, code):
        # Lấy thông tin bài tập
        assignment = Assignment.objects.get(course_code = course.code, id = id)

        try:
            # Kiểm tra nếu sinh viên đã nộp bài tập
            submission = Submission.objects.get(assignment = assignment, student = Student.objects.get(student_id = request.session['student_id']))

            context = {
                'assignment': assignment,
                'course': course,
                'submission': submission,
                'time': datetime.datetime.now(),
                'student': Student.objects.get(student_id=request.session['student_id']),
                'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
            }

            # Render trang bài tập với thông tin bài tập và nộp bài tập
            return render(request, 'main/assignment-portal.html', context)
        except:
            submission = None

        context = {
            'assignment': assignment,
            'course': course,
            'submission': submission,
            'time': datetime.datetime.now(),
            'student': Student.objects.get(student_id=request.session['student_id']),
            'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
        }

        # Render trang bài tập chỉ với thông tin bài tập (không có nộp bài tập)
        return render(request, 'main/assignment-portal.html', context)
    else:
        # Redirect đến trang đăng nhập nếu không có quyền truy cập
        return redirect('std_login')


def allAssignments(request, code):
    """
    Hiển thị danh sách tất cả bài tập.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Trang danh sách bài tập sẽ được hiển thị cho người dùng nếu người dùng là giảng viên và có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Danh sách bài tập và số lượng sinh viên trong khóa học sẽ được truy xuất và truyền vào template để hiển thị.

    """
    if is_faculty_authorised(request, code):
        # Lấy thông tin khóa học
        course = Course.objects.get(code = code)

        # Lấy danh sách bài tập
        assignments = Assignment.objects.filter(course_code = course)

        # Đếm số lượng sinh viên trong khóa học
        studentCount = Student.objects.filter(course=course).count()

        context = {
            'assignments': assignments,
            'course': course,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount
        }

        # Render trang danh sách bài tập với thông tin bài tập và số lượng sinh viên
        return render(request, 'main/all-assignments.html', context)
    else:
        # Redirect đến trang đăng nhập nếu không có quyền truy cập
        return redirect('std_login')


def allAssignmentsSTD(request, code):
    """
    Hiển thị danh sách tất cả bài tập cho sinh viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Trang danh sách bài tập sẽ được hiển thị cho sinh viên nếu sinh viên có quyền truy cập vào khóa học (được xác định bởi mã khóa học).
        - Danh sách bài tập sẽ được lấy từ cơ sở dữ liệu và truyền vào template để hiển thị.

    """
    if is_student_authorised(request, code):
        # Lấy thông tin khóa học
        course = Course.objects.get(code=code)

        # Lấy danh sách bài tập
        assignments = Assignment.objects.filter(course_code = course)

        context = {
            'assignments': assignments,
            'course': course,
            'student': Student.objects.get(student_id=request.session['student_id'])
        }

        # Render trang danh sách bài tập cho sinh viên
        return render(request, 'main/all-assignments-std.html', context)
    else:
        # Redirect đến trang đăng nhập nếu không có quyền truy cập
        return redirect('std_login')


def addSubmission(request, code, id):
    """
    Xử lý việc nộp bài tập của sinh viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest đại diện cho yêu cầu gửi đến server.
        code (int): Mã khóa học.
        id (int): ID bài tập.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        None

    Notes:
        - Hàm này xử lý việc sinh viên nộp bài tập cho một bài tập cụ thể trong khóa học.
        - Kiểm tra xem bài tập có đang mở hay không dựa trên thời hạn nộp.
        - Nếu yêu cầu gửi là POST và có tệp tin đính kèm, bài tập sẽ được tạo và lưu trong cơ sở dữ liệu với trạng thái 'Submitted'.
        - Nếu không, hiển thị trang portal của bài tập cho sinh viên.

    """
    try:
        # Lấy thông tin khóa học
        course = Course.objects.get(code = code)

        if is_student_authorised(request, code):
            # Kiểm tra xem bài tập có đang mở hay không dựa trên thời hạn nộp
            assignment = Assignment.objects.get(course_code = course.code, id = id)
            if assignment.deadline < datetime.datetime.now():
                return redirect('/assignment/' + str(code) + '/' + str(id))

            if request.method == 'POST' and request.FILES['file']:
                # Sinh viên gửi yêu cầu POST và có tệp tin đính kèm
                assignment = Assignment.objects.get(course_code=course.code, id = id)
                submission = Submission(
                    assignment=assignment,
                    student=Student.objects.get(student_id=request.session['student_id']),
                    file=request.FILES['file']
                )
                submission.status = 'Submitted'
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                # Hiển thị trang portal của bài tập cho sinh viên
                assignment = Assignment.objects.get(course_code=course.code, id = id)
                submission = Submission.objects.get(
                    assignment=assignment,
                    student=Student.objects.get(student_id=request.session['student_id'])
                )
                context = {
                    'assignment': assignment,
                    'course': course,
                    'submission': submission,
                    'time': datetime.datetime.now(),
                    'student': Student.objects.get(student_id=request.session['student_id']),
                    'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
                }
                return render(request, 'main/assignment-portal.html', context)
        else:
            # Redirect đến trang đăng nhập nếu không có quyền truy cập
            return redirect('std_login')
    except:
        return HttpResponseRedirect(request.path_info)


def viewSubmission(request, code, id):
    """
    Hiển thị danh sách bài nộp cho một bài tập cụ thể trong khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.
        code (str): Mã khóa học.
        id (int): ID của bài tập.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A

    Notes:
        - Hàm này xem danh sách các bài nộp của một bài tập cụ thể trong khóa học.
        - Kiểm tra xem người dùng có quyền truy cập là giáo viên của khóa học hay không.
        - Lấy danh sách các bài nộp và các thông tin liên quan.
        - Hiển thị trang xem danh sách bài nộp.
    """
    # Lấy thông tin về khóa học từ mã khóa học được cung cấp
    course = Course.objects.get(code = code)

    # Kiểm tra xem người dùng có quyền truy cập là giáo viên của khóa học hay không
    if is_faculty_authorised(request, code):
        try:
            # Lấy thông tin về bài tập từ ID bài tập và mã khóa học
            assignment = Assignment.objects.get(course_code_id=code, id = id)

            # Lấy danh sách các bài nộp cho bài tập đó
            submissions = Submission.objects.filter(assignment_id=assignment.id)

            # Tạo context chứa các thông tin cần thiết để hiển thị trên trang xem danh sách bài nộp
            context = {
                'course': course,
                'submissions': submissions,
                'assignment': assignment,
                'totalStudents': len(Student.objects.filter(course=course)),
                'faculty': Faculty.objects.get(faculty_id= request.session['faculty_id']),
                'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
            }

            # Trả về đối tượng HttpResponse chứa kết quả trả về cho yêu cầu
            return render(request, 'main/assignment-view.html', context)

        except:
            # Nếu có lỗi xảy ra, chuyển hướng người dùng về trang khóa học
            return redirect('/faculty/' + str(code))
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def gradeSubmission(request, code, id, sub_id):
    """
    Ghi điểm cho một bài nộp cụ thể trong khóa học và bài tập.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.
        code (str): Mã khóa học.
        id (int): ID của bài tập.
        sub_id (int): ID của bài nộp.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    try:
        # Lấy thông tin về khóa học từ mã khóa học được cung cấp
        course = Course.objects.get(code=code)

        # Kiểm tra xem người dùng có quyền truy cập là giáo viên của khóa học hay không
        if is_faculty_authorised(request, code):
            if request.method == 'POST':
                # Lấy thông tin về bài tập từ ID bài tập và mã khóa học
                assignment = Assignment.objects.get(course_code_id=code, id = id)

                # Lấy danh sách các bài nộp cho bài tập đó
                submissions = Submission.objects.filter(assignment_id=assignment.id)

                # Lấy thông tin về bài nộp cần ghi điểm
                submission = Submission.objects.get(assignment_id = id, id=sub_id)

                # Gán điểm cho bài nộp dựa trên giá trị nhập vào từ form
                submission.marks = request.POST['marks']

                # Kiểm tra nếu điểm là 0, gán lại điểm cho bài nộp là 0
                if request.POST['marks'] == 0:
                    submission.marks = 0

                # Lưu các thay đổi vào cơ sở dữ liệu
                submission.save()

                # Chuyển hướng người dùng trở lại trang hiện tại để cập nhật kết quả
                return HttpResponseRedirect(request.path_info)
            else:
                # Lấy thông tin về bài tập từ ID bài tập và mã khóa học
                assignment = Assignment.objects.get(course_code_id=code, id = id)

                # Lấy danh sách các bài nộp cho bài tập đó
                submissions = Submission.objects.filter(assignment_id=assignment.id)

                # Lấy thông tin về bài nộp cần xem/ghi điểm
                submission = Submission.objects.get(assignment_id = id, id=sub_id)

                # Tạo context chứa các thông tin cần thiết để hiển thị trên trang xem danh sách bài nộp
                context = {
                    'course': course,
                    'submissions': submissions,
                    'assignment': assignment,
                    'totalStudents': len(Student.objects.filter(course=course)),
                    'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
                    'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
                }

                # Trả về đối tượng HttpResponse chứa kết quả trả về cho yêu cầu
                return render(request, 'main/assignment-view.html', context)

        else:
            # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
            return redirect('std_login')
    except:
        # Nếu có lỗi xảy ra, chuyển hướng người dùng đến trang lỗi
        return redirect('/error/')


def addCourseMaterial(request, code):
    """
    Thêm tài liệu khóa học mới vào khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.
        code (str): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            # Xử lý yêu cầu POST - gửi biểu mẫu để thêm tài liệu khóa học
            form = MaterialForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                # Nếu biểu mẫu hợp lệ, lưu tài liệu khóa học vào cơ sở dữ liệu
                form.save()
                messages.success(request, 'New course material added')
                return redirect('/faculty/' + str(code))
            else:
                # Nếu biểu mẫu không hợp lệ, hiển thị lại biểu mẫu với thông báo lỗi
                return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
        else:
            # Xử lý yêu cầu GET - hiển thị biểu mẫu để thêm tài liệu khóa học
            form = MaterialForm()
            return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def deleteCourseMaterial(request, code, id):
    """
    Xóa tài liệu khóa học khỏi khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.
        code (str): Mã khóa học.
        id (int): ID của tài liệu khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        course_material = Material.objects.get(course_code=course, id = id)
        course_material.delete()
        messages.warning(request, 'Course material deleted')
        return redirect('/faculty/' + str(code))
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def courses(request):
    """
    Hiển thị danh sách tất cả các khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if request.session.get('student_id') or request.session.get('faculty_id'):

        courses = Course.objects.all()

        # Kiểm tra xem người dùng là sinh viên hay giảng viên
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None

        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None

        # Lấy danh sách khóa học mà sinh viên đã đăng ký (nếu là sinh viên) hoặc danh sách khóa học giảng dạy (nếu là giảng viên)
        enrolled = student.course.all() if student else None
        accessed = Course.objects.filter(
            faculty_id=faculty.faculty_id) if faculty else None

        context = {
            'faculty': faculty,
            'courses': courses,
            'student': student,
            'enrolled': enrolled,
            'accessed': accessed
        }

        return render(request, 'main/all-courses.html', context)

    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def departments(request):
    """
    Hiển thị danh sách tất cả các khoa.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if request.session.get('student_id') or request.session.get('faculty_id'):
        departments = Department.objects.all()

        # Kiểm tra xem người dùng là sinh viên hay giảng viên
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None

        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None

        context = {
            'faculty': faculty,
            'student': student,
            'deps': departments
        }

        return render(request, 'main/departments.html', context)

    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def access(request, code):
    """
    Xác thực và cho phép sinh viên truy cập vào khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.
        code (str): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if request.session.get('student_id'):
        course = Course.objects.get(code=code)
        student = Student.objects.get(student_id=request.session['student_id'])

        if request.method == 'POST':
            # Kiểm tra mã khóa nhập vào với mã khóa của khóa học
            if (request.POST['key']) == str(course.studentKey):
                student.course.add(course)
                student.save()
                return redirect('/my/')
            else:
                messages.error(request, 'Invalid key')
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, 'main/access.html', {'course': course, 'student': student})

    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def search(request):
    """
    Tìm kiếm khóa học dựa trên từ khóa nhập vào.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if request.session.get('student_id') or request.session.get('faculty_id'):
        if request.method == 'GET' and request.GET['q']:
            q = request.GET['q']
            # Tìm kiếm khóa học dựa trên mã khóa, tên khóa học, hoặc tên của khoa giảng dạy
            courses = Course.objects.filter(Q(code__icontains=q) | Q(
                name__icontains=q) | Q(faculty__name__icontains=q))

            if request.session.get('student_id'):
                student = Student.objects.get(
                    student_id=request.session['student_id'])
            else:
                student = None
            if request.session.get('faculty_id'):
                faculty = Faculty.objects.get(
                    faculty_id=request.session['faculty_id'])
            else:
                faculty = None
            enrolled = student.course.all() if student else None
            accessed = Course.objects.filter(
                faculty_id=faculty.faculty_id) if faculty else None

            context = {
                'courses': courses,
                'faculty': faculty,
                'student': student,
                'enrolled': enrolled,
                'accessed': accessed,
                'q': q
            }
            return render(request, 'main/search.html', context)
        else:
            # Nếu không có từ khóa tìm kiếm được cung cấp, chuyển hướng người dùng về trang trước đó
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePasswordPrompt(request):
    """
    Hiển thị giao diện yêu cầu thay đổi mật khẩu.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        return render(request, 'main/changePassword.html', {'student': student})
    elif request.session.get('faculty_id'):
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePhotoPrompt(request):
    """
    Hiển thị giao diện yêu cầu thay đổi ảnh đại diện.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Kiểm tra xem người dùng có phải là sinh viên hay không
    if request.session.get('student_id'):
        # Lấy thông tin sinh viên từ session
        student = Student.objects.get(student_id=request.session['student_id'])
        # Trả về giao diện thay đổi ảnh đại diện cho sinh viên
        return render(request, 'main/changePhoto.html', {'student': student})
    # Kiểm tra xem người dùng có phải là giảng viên hay không
    elif request.session.get('faculty_id'):
        # Lấy thông tin giảng viên từ session
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        # Trả về giao diện thay đổi ảnh đại diện cho giảng viên
        return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePassword(request):
    """
    Thực hiện thay đổi mật khẩu của người dùng.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Kiểm tra xem người dùng có phải là sinh viên hay không
    if request.session.get('student_id'):
        # Lấy thông tin sinh viên từ session
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if student.password == request.POST['oldPassword']:
                # Kiểm tra xem mật khẩu cũ đã đúng hay chưa
                # (Đã kiểm tra tính hợp lệ của mật khẩu mới và xác nhận mật khẩu mới ở phía client)
                student.password = request.POST['newPassword']
                student.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/profile/' + str(student.student_id))
            else:
                # Nếu mật khẩu cũ không đúng, thông báo lỗi
                messages.error(request, 'Password is incorrect. Please try again')
                return redirect('/changePassword/')
        else:
            # Trả về giao diện thay đổi mật khẩu cho sinh viên
            return render(request, 'main/changePassword.html', {'student': student})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePasswordFaculty(request):
    """
    Thực hiện thay đổi mật khẩu của giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Kiểm tra xem người dùng có phải là giảng viên hay không
    if request.session.get('faculty_id'):
        # Lấy thông tin giảng viên từ session
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if faculty.password == request.POST['oldPassword']:
                # Kiểm tra xem mật khẩu cũ đã đúng hay chưa
                # (Đã kiểm tra tính hợp lệ của mật khẩu mới và xác nhận mật khẩu mới ở phía client)
                faculty.password = request.POST['newPassword']
                faculty.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                # Nếu mật khẩu cũ không đúng, thông báo lỗi
                messages.error(request, 'Password is incorrect. Please try again')
                return redirect('/changePasswordFaculty/')
        else:
            # Trả về giao diện thay đổi mật khẩu cho giảng viên
            return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePhoto(request):
    """
    Thực hiện thay đổi ảnh đại diện của sinh viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Kiểm tra xem người dùng có phải là sinh viên hay không
    if request.session.get('student_id'):
        # Lấy thông tin sinh viên từ session
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                # Kiểm tra xem người dùng đã chọn ảnh hay chưa
                student.photo = request.FILES['photo']
                student.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/profile/' + str(student.student_id))
            else:
                # Nếu người dùng không chọn ảnh, thông báo lỗi
                messages.error(request, 'Please select a photo')
                return redirect('/changePhoto/')
        else:
            # Trả về giao diện thay đổi ảnh đại diện cho sinh viên
            return render(request, 'main/changePhoto.html', {'student': student})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def changePhotoFaculty(request):
    """
    Thực hiện thay đổi ảnh đại diện của giảng viên.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Kiểm tra xem người dùng có phải là giảng viên hay không
    if request.session.get('faculty_id'):
        # Lấy thông tin giảng viên từ session
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                # Kiểm tra xem người dùng đã chọn ảnh hay chưa
                faculty.photo = request.FILES['photo']
                faculty.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                # Nếu người dùng không chọn ảnh, thông báo lỗi
                messages.error(request, 'Please select a photo')
                return redirect('/changePhotoFaculty/')
        else:
            # Trả về giao diện thay đổi ảnh đại diện cho giảng viên
            return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        # Nếu người dùng không có quyền truy cập, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def guestStudent(request):
    """
    Thực hiện đăng nhập với tư cách là Sinh viên Khách.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Xóa thông tin phiên trước đó
    request.session.flush()
    try:
        # Lấy thông tin Sinh viên Khách từ cơ sở dữ liệu
        student = Student.objects.get(name='Guest Student')
        # Lưu student_id của Sinh viên Khách vào session
        request.session['student_id'] = str(student.student_id)
        # Chuyển hướng người dùng đến trang "myCourses"
        return redirect('myCourses')
    except:
        # Nếu không tìm thấy thông tin Sinh viên Khách trong cơ sở dữ liệu, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')


def guestFaculty(request):
    """
    Thực hiện đăng nhập với tư cách là Giảng viên Khách.

    Args:
        request (HttpRequest): Đối tượng HttpRequest chứa thông tin về yêu cầu HTTP.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa kết quả trả về cho yêu cầu.

    Raises:
        N/A
    """

    # Xóa thông tin phiên trước đó
    request.session.flush()
    try:
        # Lấy thông tin Giảng viên Khách từ cơ sở dữ liệu
        faculty = Faculty.objects.get(name='Guest Faculty')
        # Lưu faculty_id của Giảng viên Khách vào session
        request.session['faculty_id'] = str(faculty.faculty_id)
        # Chuyển hướng người dùng đến trang "facultyCourses"
        return redirect('facultyCourses')
    except:
        # Nếu không tìm thấy thông tin Giảng viên Khách trong cơ sở dữ liệu, chuyển hướng người dùng về trang đăng nhập
        return redirect('std_login')