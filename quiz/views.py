import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, StudentAnswer
from main.models import Student, Course, Faculty
from main.views import is_faculty_authorised, is_student_authorised
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, F, FloatField, Q, Prefetch
from django.db.models.functions import Cast


def quiz(request, code):
    """
    Hiển thị trang tạo bài trắc nghiệm cho một khóa học.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.

    Returns:
        Nếu request method là POST và dữ liệu hợp lệ, chuyển hướng đến trang thêm câu hỏi cho bài trắc nghiệm mới được tạo.
        Nếu request method là GET hoặc người dùng không có quyền truy cập, hiển thị trang lỗi.
        Nếu không tìm thấy khóa học tương ứng với mã khóa học đã cho, hiển thị trang lỗi.

    Raises:
        Không có exception được raise.

    """
    try:
        course = Course.objects.get(code=code)
        if is_faculty_authorised(request, code):
            if request.method == 'POST':
                # Xử lý thông tin bài trắc nghiệm được submit
                title = request.POST.get('title')
                description = request.POST.get('description')
                start = request.POST.get('start')
                end = request.POST.get('end')
                publish_status = request.POST.get('checkbox')
                quiz = Quiz(title=title, description=description, start=start,
                            end=end, publish_status=publish_status, course=course)
                quiz.save()
                return redirect('addQuestion', code=code, quiz_id=quiz.id)
            else:
                # Hiển thị trang tạo bài trắc nghiệm
                return render(request, 'quiz/quiz.html', {'course': course, 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
        else:
            # Người dùng không có quyền truy cập
            return redirect('std_login')
    except:
        # Không tìm thấy khóa học
        return render(request, 'error.html')


def addQuestion(request, code, quiz_id):
    """
    Thêm câu hỏi vào bài trắc nghiệm.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.
        quiz_id: ID của bài trắc nghiệm.

    Returns:
        Nếu request method là POST và dữ liệu hợp lệ, câu hỏi mới được thêm vào bài trắc nghiệm và chuyển hướng đến trang thêm câu hỏi khác hoặc danh sách tất cả các bài trắc nghiệm.
        Nếu request method là GET, hiển thị trang thêm câu hỏi cho bài trắc nghiệm.
        Nếu người dùng không có quyền truy cập, chuyển hướng đến trang đăng nhập.
        Nếu không tìm thấy khóa học hoặc bài trắc nghiệm tương ứng, hiển thị trang lỗi.

    Raises:
        Không có exception được raise.

    """
    try:
        course = Course.objects.get(code=code)
        if is_faculty_authorised(request, code):
            quiz = Quiz.objects.get(id=quiz_id)
            if request.method == 'POST':
                # Xử lý thông tin câu hỏi được submit
                question = request.POST.get('question')
                option1 = request.POST.get('option1')
                option2 = request.POST.get('option2')
                option3 = request.POST.get('option3')
                option4 = request.POST.get('option4')
                answer = request.POST.get('answer')
                marks = request.POST.get('marks')
                explanation = request.POST.get('explanation')
                question = Question(question=question, option1=option1, option2=option2,
                                    option3=option3, option4=option4, answer=answer, quiz=quiz, marks=marks, explanation=explanation)
                question.save()
                messages.success(request, 'Question added successfully')
            else:
                # Hiển thị trang thêm câu hỏi cho bài trắc nghiệm
                return render(request, 'quiz/addQuestion.html', {'course': course, 'quiz': quiz, 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
            if 'saveOnly' in request.POST:
                # Chuyển hướng đến danh sách tất cả các bài trắc nghiệm
                return redirect('allQuizzes', code=code)
            # Hiển thị trang thêm câu hỏi cho bài trắc nghiệm
            return render(request, 'quiz/addQuestion.html', {'course': course, 'quiz': quiz, 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
        else:
            # Người dùng không có quyền truy cập
            return redirect('std_login')
    except:
        # Không tìm thấy khóa học hoặc bài trắc nghiệm
        return render(request, 'error.html')


def allQuizzes(request, code):
    """
    Hiển thị danh sách tất cả các bài trắc nghiệm của một khóa học.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.

    Returns:
        Nếu người dùng có quyền truy cập, hiển thị trang danh sách tất cả các bài trắc nghiệm của khóa học.
        Nếu người dùng không có quyền truy cập, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_faculty_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy danh sách các bài trắc nghiệm của khóa học
        quizzes = Quiz.objects.filter(course=course)
        
        # Cập nhật thông tin cho mỗi bài trắc nghiệm
        for quiz in quizzes:
            # Đếm số câu hỏi trong bài trắc nghiệm
            quiz.total_questions = Question.objects.filter(quiz=quiz).count()
            
            # Kiểm tra xem bài trắc nghiệm đã bắt đầu hay chưa
            if quiz.start < datetime.datetime.now():
                quiz.started = True
            else:
                quiz.started = False
            quiz.save()
        
        # Hiển thị trang danh sách tất cả các bài trắc nghiệm của khóa học
        return render(request, 'quiz/allQuizzes.html', {'course': course, 'quizzes': quizzes, 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
    else:
        # Người dùng không có quyền truy cập, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def myQuizzes(request, code):
    """
    Hiển thị danh sách các bài trắc nghiệm của sinh viên trong một khóa học.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.

    Returns:
        Nếu người dùng là sinh viên và có quyền truy cập, hiển thị trang danh sách các bài trắc nghiệm của sinh viên trong khóa học.
        Nếu người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_student_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy danh sách các bài trắc nghiệm của khóa học
        quizzes = Quiz.objects.filter(course=course)
        
        # Lấy thông tin sinh viên dựa trên session
        student = Student.objects.get(student_id=request.session['student_id'])
        
        # Xác định các bài trắc nghiệm đang diễn ra và các bài trắc nghiệm đã kết thúc
        active_quizzes = []
        previous_quizzes = []
        for quiz in quizzes:
            if quiz.end < timezone.now() or quiz.studentanswer_set.filter(student=student).exists():
                previous_quizzes.append(quiz)
            else:
                active_quizzes.append(quiz)

        # Thêm cờ "attempted" cho từng bài trắc nghiệm
        for quiz in quizzes:
            quiz.attempted = quiz.studentanswer_set.filter(student=student).exists()

        # Thêm thông tin tổng điểm đạt được, phần trăm, và số câu hỏi cho các bài trắc nghiệm đã kết thúc
        for quiz in previous_quizzes:
            student_answers = quiz.studentanswer_set.filter(student=student)
            total_marks_obtained = sum([student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0 for student_answer in student_answers])
            quiz.total_marks_obtained = total_marks_obtained
            quiz.total_marks = sum([question.marks for question in quiz.question_set.all()])
            quiz.percentage = round(total_marks_obtained / quiz.total_marks * 100, 2) if quiz.total_marks != 0 else 0
            quiz.total_questions = quiz.question_set.count()

        # Thêm số câu hỏi cho các bài trắc nghiệm đang diễn ra
        for quiz in active_quizzes:
            quiz.total_questions = quiz.question_set.count()

        # Hiển thị trang danh sách các bài trắc nghiệm của sinh viên trong khóa học
        return render(request, 'quiz/myQuizzes.html', {
            'course': course,
            'quizzes': quizzes,
            'active_quizzes': active_quizzes,
            'previous_quizzes': previous_quizzes,
            'student': student,
        })
    else:
        # Người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def startQuiz(request, code, quiz_id):
    """
    Bắt đầu bài trắc nghiệm và hiển thị trang bắt đầu làm bài.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.
        quiz_id: ID của bài trắc nghiệm được chọn.

    Returns:
        Nếu người dùng là sinh viên và có quyền truy cập, hiển thị trang bắt đầu làm bài trắc nghiệm.
        Nếu người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_student_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy thông tin bài trắc nghiệm dựa trên ID bài trắc nghiệm
        quiz = Quiz.objects.get(id=quiz_id)
        
        # Lấy danh sách các câu hỏi của bài trắc nghiệm
        questions = Question.objects.filter(quiz=quiz)
        
        # Đếm số câu hỏi
        total_questions = questions.count()

        # Tính tổng điểm của bài trắc nghiệm
        marks = 0
        for question in questions:
            marks += question.marks
        quiz.total_marks = marks

        # Hiển thị trang bắt đầu làm bài trắc nghiệm
        return render(request, 'quiz/portalStdNew.html', {
            'course': course,
            'quiz': quiz,
            'questions': questions,
            'total_questions': total_questions,
            'student': Student.objects.get(student_id=request.session['student_id'])
        })
    else:
        # Người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def studentAnswer(request, code, quiz_id):
    """
    Xử lý và lưu câu trả lời của sinh viên cho bài trắc nghiệm.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.
        quiz_id: ID của bài trắc nghiệm được chọn.

    Returns:
        Nếu người dùng là sinh viên và có quyền truy cập, sau khi lưu câu trả lời thành công, chuyển hướng đến trang danh sách bài trắc nghiệm của sinh viên.
        Nếu người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_student_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy thông tin bài trắc nghiệm dựa trên ID bài trắc nghiệm
        quiz = Quiz.objects.get(id=quiz_id)
        
        # Lấy danh sách các câu hỏi của bài trắc nghiệm
        questions = Question.objects.filter(quiz=quiz)
        
        # Lấy thông tin sinh viên
        student = Student.objects.get(student_id=request.session['student_id'])

        # Lưu câu trả lời của sinh viên cho từng câu hỏi
        for question in questions:
            answer = request.POST.get(str(question.id))
            student_answer = StudentAnswer(student=student, quiz=quiz, question=question,
                                           answer=answer, marks=question.marks if answer == question.answer else 0)
            # Ngăn không cho câu trả lời bị trùng lặp và ngăn không cho sinh viên làm nhiều lần
            try:
                student_answer.save()
            except:
                # Nếu có lỗi xảy ra khi lưu câu trả lời, chuyển hướng đến trang danh sách bài trắc nghiệm của sinh viên
                redirect('myQuizzes', code=code)
        
        # Sau khi lưu câu trả lời thành công, chuyển hướng đến trang danh sách bài trắc nghiệm của sinh viên
        return redirect('myQuizzes', code=code)
    else:
        # Người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def quizResult(request, code, quiz_id):
    """
    Hiển thị kết quả của bài trắc nghiệm cho sinh viên.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.
        quiz_id: ID của bài trắc nghiệm được chọn.

    Returns:
        Nếu người dùng là sinh viên và có quyền truy cập, hiển thị trang kết quả của bài trắc nghiệm cho sinh viên.
        Nếu người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_student_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy thông tin bài trắc nghiệm dựa trên ID bài trắc nghiệm
        quiz = Quiz.objects.get(id=quiz_id)
        
        # Lấy danh sách câu hỏi của bài trắc nghiệm
        questions = Question.objects.filter(quiz=quiz)
        
        try:
            # Lấy thông tin sinh viên
            student = Student.objects.get(
                student_id=request.session['student_id'])
            
            # Lấy danh sách câu trả lời của sinh viên cho bài trắc nghiệm
            student_answers = StudentAnswer.objects.filter(
                student=student, quiz=quiz)
            
            # Tính tổng số điểm sinh viên đạt được
            total_marks_obtained = 0
            for student_answer in student_answers:
                total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
            
            # Cập nhật thông tin về tổng số điểm và tỷ lệ phần trăm
            quiz.total_marks_obtained = total_marks_obtained
            quiz.total_marks = 0
            for question in questions:
                quiz.total_marks += question.marks
            quiz.percentage = (total_marks_obtained / quiz.total_marks) * 100
            quiz.percentage = round(quiz.percentage, 2)
        
        except:
            # Nếu không tìm thấy thông tin sinh viên hoặc câu trả lời của sinh viên, đặt các giá trị mặc định
            quiz.total_marks_obtained = 0
            quiz.total_marks = 0
            quiz.percentage = 0

        # Thêm thông tin câu trả lời của sinh viên cho từng câu hỏi
        for question in questions:
            student_answer = StudentAnswer.objects.get(
                student=student, question=question)
            question.student_answer = student_answer.answer

        # Lấy danh sách câu trả lời của sinh viên cho bài trắc nghiệm
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        
        # Cập nhật thông tin về thời gian làm bài và thời gian nộp bài
        for student_answer in student_answers:
            quiz.time_taken = student_answer.created_at - quiz.start
            quiz.time_taken = quiz.time_taken.total_seconds()
            quiz.time_taken = round(quiz.time_taken, 2)
            quiz.submission_time = student_answer.created_at.strftime(
                "%a, %d-%b-%y at %I:%M %p")
        
        # Hiển thị trang kết quả của bài trắc nghiệm cho sinh viên
        return render(request, 'quiz/quizResult.html', {'course': course, 'quiz': quiz, 'questions': questions, 'student': student})
    else:
        # Người dùng không có quyền truy cập hoặc không phải là sinh viên, chuyển hướng đến trang đăng nhập
        return redirect('std_login')


def quizSummary(request, code, quiz_id):
    """
    Hiển thị tổng kết của bài trắc nghiệm cho giảng viên.

    Args:
        request: Đối tượng HttpRequest đại diện cho request được gửi đến server.
        code: Mã khóa học của khóa học được chọn.
        quiz_id: ID của bài trắc nghiệm được chọn.

    Returns:
        Nếu người dùng là giảng viên và có quyền truy cập, hiển thị trang tổng kết của bài trắc nghiệm cho giảng viên.
        Nếu người dùng không có quyền truy cập hoặc không phải là giảng viên, chuyển hướng đến trang đăng nhập.

    Raises:
        Không có exception được raise.

    """
    if is_faculty_authorised(request, code):
        # Lấy thông tin khóa học dựa trên mã khóa học
        course = Course.objects.get(code=code)
        
        # Lấy thông tin bài trắc nghiệm dựa trên ID bài trắc nghiệm
        quiz = Quiz.objects.get(id=quiz_id)

        # Lấy danh sách câu hỏi của bài trắc nghiệm
        questions = Question.objects.filter(quiz=quiz)
        
        # Lấy thời gian hiện tại
        time = datetime.datetime.now()
        
        # Lấy số lượng sinh viên đã đăng ký khóa học
        total_students = Student.objects.filter(course=course).count()
        
        # Đếm số lần câu trả lời A, B, C, D cho từng câu hỏi
        for question in questions:
            question.A = StudentAnswer.objects.filter(
                question=question, answer='A').count()
            question.B = StudentAnswer.objects.filter(
                question=question, answer='B').count()
            question.C = StudentAnswer.objects.filter(
                question=question, answer='C').count()
            question.D = StudentAnswer.objects.filter(
                question=question, answer='D').count()
        
        # Lấy danh sách sinh viên đã làm bài và điểm số của họ
        students = Student.objects.filter(course=course)
        for student in students:
            student_answers = StudentAnswer.objects.filter(
                student=student, quiz=quiz)
            total_marks_obtained = 0
            for student_answer in student_answers:
                total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
            student.total_marks_obtained = total_marks_obtained

        if request.method == 'POST':
            # Cập nhật trạng thái công bố cho bài trắc nghiệm và lưu vào cơ sở dữ liệu
            quiz.publish_status = True
            quiz.save()
            return redirect('quizSummary', code=code, quiz_id=quiz.id)

        # Kiểm tra xem sinh viên đã làm bài trắc nghiệm hay chưa
        for student in students:
            if StudentAnswer.objects.filter(student=student, quiz=quiz).count() > 0:
                student.attempted = True
            else:
                student.attempted = False
        
        # Lấy thời gian nộp bài và định dạng thời gian
        for student in students:
            student_answers = StudentAnswer.objects.filter(
                student=student, quiz=quiz)
            for student_answer in student_answers:
                student.submission_time = student_answer.created_at.strftime(
                    "%a, %d-%b-%y at %I:%M %p")

        # Tạo context chứa các thông tin cần thiết để hiển thị trang tổng kết cho giảng viên
        context = {'course': course, 'quiz': quiz, 'questions': questions, 'time': time, 'total_students': total_students,
                   'students': students, 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])}
        return render(request, 'quiz/quizSummaryFaculty.html', context)
    else:
        # Người dùng không có quyền truy cập hoặc không phải là giảng viên, chuyển hướng đến trang đăng nhập
        return redirect('std_login')