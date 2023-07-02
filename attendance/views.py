from django.contrib import messages
from django.shortcuts import render, redirect
from . models import Attendance
from main.models import Student, Course, Faculty
from main.views import is_faculty_authorised


def attendance(request, code):
    """
    Xem danh sách điểm danh cho một khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa trang HTML hiển thị danh sách điểm danh.
    """
    if is_faculty_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code = code)
        # Lấy danh sách sinh viên của khóa học
        students = Student.objects.filter(course__code = code)

        return render(request, 'attendance/attendance.html', {'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})


def createRecord(request, code):
    """
    Tạo bản ghi điểm danh mới cho một khóa học.

    Args:
        request (HttpRequest): Đối tượng HttpRequest.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa trang HTML hiển thị kết quả sau khi tạo bản ghi điểm danh.

    Raises:
        Redirect: Nếu người dùng không được ủy quyền hoặc chưa đăng nhập, chuyển hướng đến trang đăng nhập.
    """
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            # Lấy ngày điểm danh từ dữ liệu POST
            date = request.POST['dateCreate']
            # Lấy thông tin khóa học dựa trên mã khóa học
            course = Course.objects.get(code = code)
            # Lấy danh sách sinh viên của khóa học
            students = Student.objects.filter(course__code = code)
            # Kiểm tra xem bản ghi điểm danh đã tồn tại cho ngày đã cho hay chưa
            if Attendance.objects.filter(date = date, course = course).exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'error': "Attendance record already exists for the date " + date})
            else:
                # Tạo bản ghi điểm danh cho từng sinh viên trong khóa học
                for student in students:
                    attendance = Attendance(
                        student=student, course = course, date = date, status = False)
                    attendance.save()

                messages.success(
                    request, 'Attendance record created successfully for the date ' + date)
                return redirect('/attendance/' + str(code))
        else:
            return redirect('/attendance/' + str(code))
    else:
        return redirect('std_login')


def loadAttendance(request, code):
    """
    Tải danh sách điểm danh cho một khóa học và một ngày nhất định.

    Args:
        request (HttpRequest): Đối tượng HttpRequest.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa trang HTML hiển thị danh sách điểm danh.

    Raises:
        Redirect: Nếu người dùng không được ủy quyền hoặc chưa đăng nhập, chuyển hướng đến trang đăng nhập.
    """
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            # Lấy ngày điểm danh từ dữ liệu POST
            date = request.POST['date']
            # Lấy thông tin khóa học dựa trên mã khóa học
            course = Course.objects.get(code = code)
            # Lấy danh sách sinh viên của khóa học
            students = Student.objects.filter(course__code = code)
            # Lấy danh sách điểm danh dựa trên khóa học và ngày điểm danh
            attendance = Attendance.objects.filter(course = course, date = date)
            # Kiểm tra xem có bản ghi điểm danh nào tồn tại cho ngày đã cho hay không
            if attendance.exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'attendance': attendance, 'date': date})
            else:
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'error': 'Could not load. Attendance record does not exist for the date ' + date})

    else:
        return redirect('std_login')


def submitAttendance(request, code):
    """
    Gửi điểm danh cho một khóa học và một ngày nhất định.

    Args:
        request (HttpRequest): Đối tượng HttpRequest.
        code (int): Mã khóa học.

    Returns:
        HttpResponse: Đối tượng HttpResponse chứa trang HTML hiển thị kết quả sau khi gửi điểm danh.

    Raises:
        Redirect: Nếu người dùng không được ủy quyền hoặc chưa đăng nhập, chuyển hướng đến trang đăng nhập.
    """
    try:
        # Lấy danh sách sinh viên của khóa học
        students = Student.objects.filter(course__code = code)
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code = code)

        if request.method == 'POST':
            # Lấy ngày điểm danh từ dữ liệu POST
            date = request.POST['datehidden']
            for student in students:
                # Lấy bản ghi điểm danh dựa trên sinh viên, khóa học và ngày điểm danh
                attendance = Attendance.objects.get(student = student, course = course, date = date)
                if request.POST.get(str(student.student_id)) == '1':
                    # Đánh dấu sinh viên có mặt
                    attendance.status = True
                else:
                    # Đánh dấu sinh viên vắng mặt
                    attendance.status = False
                attendance.save()

            # Gửi thông báo thành công
            messages.success(
                request, 'Attendance record submitted successfully for the date ' + date)
            return redirect('/attendance/' + str(code))
        else:
            # Hiển thị trang HTML điểm danh
            return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})
    except:
        # Hiển thị trang HTML với thông báo lỗi
        return render(request, 'attendance/attendance.html', {'code': code, 'error': "Error! could not save", 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})
