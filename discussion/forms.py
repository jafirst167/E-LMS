from django import forms
from .models import StudentDiscussion, FacultyDiscussion


class StudentDiscussionForm(forms.ModelForm):
    """
    Form để tạo bài thảo luận của sinh viên.

    Attributes:
        model (Model): Model liên kết với form.
        fields (list): Danh sách các trường trong form.
        widgets (dict): Định dạng các trường trong form.
    """
    def __init__(self, *args, **kwargs):
        """
        Khởi tạo form.

        Args:
            *args: Danh sách các đối số vị trí.
            **kwargs: Danh sách các đối số từ khóa.
        """
        super(StudentDiscussionForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True
        self.fields['content'].label = ''

    class Meta:
        """
        Lớp Meta của form.

        Attributes:
            model (Model): Model liên kết với form.
            fields (list): Danh sách các trường trong form.
            widgets (dict): Định dạng các trường trong form.
        """
        model = StudentDiscussion
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'id': 'content', 'name': 'content', 'placeholder': 'Write message...', 'type': 'text'}),
        }


class FacultyDiscussionForm(forms.ModelForm):
    """
    Form để tạo bài thảo luận của giảng viên.

    Attributes:
        model (Model): Model liên kết với form.
        fields (list): Danh sách các trường trong form.
        widgets (dict): Định dạng các trường trong form.
    """
    def __init__(self, *args, **kwargs):
        """
        Khởi tạo form.

        Args:
            *args: Danh sách các đối số vị trí.
            **kwargs: Danh sách các đối số từ khóa.
        """
        super(FacultyDiscussionForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True
        self.fields['content'].label = ''

    class Meta:
        """
        Lớp Meta của form.

        Attributes:
            model (Model): Model liên kết với form.
            fields (list): Danh sách các trường trong form.
            widgets (dict): Định dạng các trường trong form.
        """
        model = FacultyDiscussion
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'id': 'content', 'name': 'content', 'placeholder': 'Write message...', 'type': 'text'}),
        }