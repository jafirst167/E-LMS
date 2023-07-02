from django.urls import path
from . import views

"""
Cấu hình URL trong Django

Tệp này xác định các mẫu URL và liên kết chúng với các view trong ứng dụng.

Mỗi mẫu URL được xác định bằng cách sử dụng hàm `path()`.
Mỗi mẫu URL được liên kết với một hàm xử lý yêu cầu từ người dùng.
Tất cả các mẫu URL được định nghĩa trong danh sách `urlpatterns`.

Danh sách mẫu URL:

- '' : Trang đăng nhập cho sinh viên (views.std_login).
- 'my/' : Trang hiển thị các khóa học của một sinh viên (views.myCourses).
- 'facultyCourses/' : Trang hiển thị các khóa học của một giảng viên (views.facultyCourses).
- 'login/' : Trang đăng nhập cho sinh viên (views.std_login).
- 'logout/' : Trang đăng xuất (views.std_logout).
- 'my/<int:code>/' : Trang khóa học cụ thể cho một sinh viên (views.course_page).
- 'profile/<str:id>/' : Trang hồ sơ cho một sinh viên (views.profile).
- 'facultyProfile/<str:id>/' : Trang hồ sơ cho một giảng viên (views.profile_faculty).
- 'faculty/<int:code>/' : Trang khóa học cụ thể cho một giảng viên (views.course_page_faculty).
- 'addAnnouncement/<int:code>/' : Trang thêm thông báo (views.addAnnouncement).
- 'announcement/<int:code>/<int:id>/' : Trang xóa thông báo (views.deleteAnnouncement).
- 'edit/<int:code>/<int:id>/' : Trang chỉnh sửa thông báo (views.editAnnouncement).
- 'update/<int:code>/<int:id>/' : Trang cập nhật thông báo (views.updateAnnouncement).
- 'addAssignment/<int:code>/' : Trang thêm bài tập (views.addAssignment).
- 'assignment/<int:code>/<int:id>/' : Trang bài tập cụ thể (views.assignmentPage).
- 'assignments/<int:code>/' : Trang tất cả các bài tập (views.allAssignments).
- 'student-assignments/<int:code>/' : Trang tất cả các bài tập cho sinh viên (views.allAssignmentsSTD).
- 'addSubmission/<int:code>/<int:id>/' : Trang thêm bài nộp (views.addSubmission).
- 'submission/<int:code>/<int:id>/' : Trang xem bài nộp (views.viewSubmission).
- 'gradeSubmission/<int:code>/<int:id>/<int:sub_id>' : Trang đánh giá bài nộp (views.gradeSubmission).
- 'course-material/<int:code>/' : Trang thêm tài liệu khóa học (views.addCourseMaterial).
- 'course-material/<int:code>/<int:id>/' : Trang xóa tài liệu khóa học (views.deleteCourseMaterial).
- 'courses/' : Trang hiển thị tất cả các khóa học (views.courses).
- 'departments/' : Trang hiển thị tất cả các khoa (views.departments).
- 'access/<int:code>/' : Trang truy cập (views.access).
- 'changePasswordPrompt/' : Trang yêu cầu thay đổi mật khẩu (views.changePasswordPrompt).
- 'changePhotoPrompt/' : Trang yêu cầu thay đổi ảnh đại diện (views.changePhotoPrompt).
- 'changePassword/' : Trang thay đổi mật khẩu (views.changePassword).
- 'changePasswordFaculty/' : Trang thay đổi mật khẩu cho giảng viên (views.changePasswordFaculty).
- 'changePhoto/' : Trang thay đổi ảnh đại diện (views.changePhoto).
- 'changePhotoFaculty/' : Trang thay đổi ảnh đại diện cho giảng viên (views.changePhotoFaculty).
- 'search/' : Trang tìm kiếm (views.search).
- 'error/' : Trang lỗi (views.error).
"""

urlpatterns = [
    path('', views.std_login, name = 'std_login'),
    path('my/', views.myCourses, name = 'myCourses'),
    path('facultyCourses/', views.facultyCourses, name = 'facultyCourses'),
    path('login/', views.std_login, name = 'std_login'),
    path('logout/', views.std_logout, name = 'std_logout'),
    path('my/<int:code>/', views.course_page, name = 'course'),
    path('profile/<str:id>/', views.profile, name = 'profile'),
    path('facultyProfile/<str:id>/', views.profile, name = 'profile_faculty'),
    path('faculty/<int:code>/', views.course_page_faculty, name = 'faculty'),
    path('addAnnouncement/<int:code>/', views.addAnnouncement, name = 'addAnnouncement'),
    path('announecement/<int:code>/<int:id>/', views.deleteAnnouncement, name = 'deleteAnnouncement'),
    path('edit/<int:code>/<int:id>/', views.editAnnouncement, name = 'editAnnouncement'),
    path('update/<int:code>/<int:id>/', views.updateAnnouncement, name = 'updateAnnouncement'),
    path('addAssignment/<int:code>/', views.addAssignment, name = 'addAssignment'),
    path('assignment/<int:code>/<int:id>/', views.assignmentPage, name = 'assignmentPage'),
    path('assignments/<int:code>/', views.allAssignments, name = 'allAssignments'),
    path('student-assignments/<int:code>/', views.allAssignmentsSTD, name = 'student-assignments'),
    path('addSubmission/<int:code>/<int:id>/', views.addSubmission, name = 'addSubmission'),
    path('submission/<int:code>/<int:id>/', views.viewSubmission, name = 'submission'),
    path('gradeSubmission/<int:code>/<int:id>/<int:sub_id>', views.gradeSubmission, name = 'gradeSubmission'),
    path('course-material/<int:code>/', views.addCourseMaterial, name = 'addCourseMaterial'),
    path('course-material/<int:code>/<int:id>/', views.deleteCourseMaterial, name = 'deleteCourseMaterial'),
    path('courses/', views.courses, name = 'courses'),
    path('departments/', views.departments, name = 'departments'),
    path('access/<int:code>/', views.access, name = 'access'),
    path('changePasswordPrompt/', views.changePasswordPrompt, name = 'changePasswordPrompt'),
    path('changePhotoPrompt/', views.changePhotoPrompt, name = 'changePhotoPrompt'),
    path('changePassword/', views.changePassword, name = 'changePassword'),
    path('changePasswordFaculty/', views.changePasswordFaculty, name = 'changePasswordFaculty'),
    path('changePhoto/', views.changePhoto, name = 'changePhoto'),
    path('changePhotoFaculty/', views.changePhotoFaculty, name = 'changePhotoFaculty'),
    path('search/', views.search, name = 'search'),
    path('error/', views.error, name = 'error'),
]