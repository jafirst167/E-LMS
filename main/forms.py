from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Announcement, Assignment, Material


class AnnouncementForm(forms.ModelForm):
    """
    Biểu mẫu để tạo thông báo (Announcement).

    Thuộc tính:
        - description: Trường nhập nội dung thông báo.

    Widgets:
        - description: FroalaEditor, trình soạn thảo văn bản cho trường description.
    """

    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)

        # Thiết lập thuộc tính bắt buộc cho trường 'description'
        self.fields['description'].required = True

        # Xóa nhãn cho trường 'description'
        self.fields['description'].label = ''

    class Meta:
        model = Announcement  # Mô hình liên kết với biểu mẫu
        fields = ['description']  # Các trường hiển thị trong biểu mẫu
        widgets = {
            # Sử dụng Froala Editor widget cho trường 'description'
            'description': FroalaEditor(),
        }


class AssignmentForm(forms.ModelForm):
    """
    Biểu mẫu để tạo bài tập (Assignment).

    Thuộc tính:
        - title: Trường nhập tiêu đề bài tập.
        - description: Trường nhập nội dung bài tập.
        - deadline: Trường chọn thời hạn nộp bài.
        - marks: Trường nhập điểm cho bài tập.
        - file: Trường tải lên tệp tin đính kèm (không bắt buộc).

    Widgets:
        - description: FroalaEditor, trình soạn thảo văn bản cho trường description.
        - title: TextInput, trường nhập tiêu đề với các thuộc tính CSS.
        - deadline: DateTimeInput, trường chọn thời gian với các thuộc tính CSS.
        - marks: NumberInput, trường nhập điểm với các thuộc tính CSS.
        - file: FileInput, trường tải lên tệp tin đính kèm.
    """

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ''
        self.fields['file'].required = False

    class Meta:
        model = Assignment
        fields = ('title', 'description', 'deadline', 'marks', 'file')
        widgets = {
            'description': FroalaEditor(),
            'title': forms.TextInput(attrs = {'class': 'form-control mt-1', 'id': 'title', 'name': 'title', 'placeholder': 'Title'}),
            'deadline': forms.DateTimeInput(attrs = {'class': 'form-control mt-1', 'id': 'deadline', 'name': 'deadline', 'type': 'datetime-local'}),
            'marks': forms.NumberInput(attrs = {'class': 'form-control mt-1', 'id': 'marks', 'name': 'marks', 'placeholder': 'Marks'}),
            'file': forms.FileInput(attrs = {'class': 'form-control mt-1', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }


class MaterialForm(forms.ModelForm):
    """
    Biểu mẫu để tạo tài liệu (Material).

    Thuộc tính:
        - description: Trường nhập nội dung tài liệu.
        - file: Trường tải lên tệp tin đính kèm (không bắt buộc).

    Widgets:
        - description: FroalaEditor, trình soạn thảo văn bản cho trường description.
        - file: FileInput, trường tải lên tệp tin đính kèm.
    """

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ""
        self.fields['file'].required = False

    class Meta:
        model = Material
        fields = ('description', 'file')
        widgets = {
            'description': FroalaEditor(),
            'file': forms.FileInput(attrs = {'class': 'form-control', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }