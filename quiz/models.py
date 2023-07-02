from venv import create
from django.db import models
from main.models import Student, Course


# Create your models here.
class Quiz(models.Model):
    """Đại diện cho một bài trắc nghiệm trong hệ thống."""
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_status = models.BooleanField(default=False, null=True, blank=True)
    started = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        """Trả về một chuỗi biểu diễn cho đối tượng Quiz."""
        return self.title

    def duration(self):
        """Trả về thời lượng của bài trắc nghiệm."""
        return self.end - self.start
        
    def duration_in_seconds(self):
        """Trả về thời lượng của bài trắc nghiệm tính bằng giây."""
        return (self.end - self.start).total_seconds()

    def total_questions(self):
        """Trả về tổng số câu hỏi trong bài trắc nghiệm."""
        return Question.objects.filter(quiz=self).count()

    def question_sl(self):
        """Trả về số câu hỏi hiện tại của bài trắc nghiệm."""
        return Question.objects.filter(quiz=self).count() + 1

    def total_marks(self):
        """Trả về tổng số điểm của bài trắc nghiệm."""
        return Question.objects.filter(quiz=self).aggregate(total_marks=models.Sum('marks'))['total_marks']

    def starts(self):
        """Trả về thời điểm bắt đầu của bài trắc nghiệm dưới dạng chuỗi định dạng."""
        return self.start.strftime("%a, %d-%b-%y at %I:%M %p")

    def ends(self):
        """Trả về thời điểm kết thúc của bài trắc nghiệm dưới dạng chuỗi định dạng."""
        return self.end.strftime("%a, %d-%b-%y at %I:%M %p")

    def attempted_students(self):
        """Trả về số lượng sinh viên đã tham gia làm bài trắc nghiệm."""
        return Student.objects.filter(studentanswer__quiz=self).distinct().count()


class Question(models.Model):
    """Đại diện cho một câu hỏi trong bài trắc nghiệm."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    marks = models.IntegerField(default=0, null=False)
    option1 = models.TextField(null=False, blank=False, default='',)
    option2 = models.TextField(null=False, blank=False, default='')
    option3 = models.TextField(null=False, blank=False, default='')
    option4 = models.TextField(null=False, blank=False, default='')
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='A')
    explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        """Trả về một chuỗi biểu diễn cho đối tượng Question."""
        return self.question

    def get_answer(self):
        """Trả về câu trả lời chính xác cho câu hỏi."""
        case = {
            'A': self.option1,
            'B': self.option2,
            'C': self.option3,
            'D': self.option4,
        }
        return case[self.answer]

    def total_correct_answers(self):
        """Trả về số lượng câu trả lời đúng cho câu hỏi."""
        return StudentAnswer.objects.filter(question=self, answer=self.answer).count()

    def total_wrong_answers(self):
        """Trả về số lượng câu trả lời sai cho câu hỏi."""
        return StudentAnswer.objects.filter(question=self).exclude(answer=self.answer).count()


class StudentAnswer(models.Model):
    """Đại diện cho câu trả lời của một sinh viên trong bài trắc nghiệm."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='', null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        """Trả về một chuỗi biểu diễn cho đối tượng StudentAnswer."""
        return self.student.name + ' ' + self.quiz.title + ' ' + self.question.question

    class Meta:
        unique_together = ('student', 'quiz', 'question')