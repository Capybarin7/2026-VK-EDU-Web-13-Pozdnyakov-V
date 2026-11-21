from django import forms
from .models import Question, Answer, Tag, QuestionTag
class AskForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tags (Optional: Add tags separated by commas)...', 'class': 'form-control'})
    )
    class Meta:
        model = Question
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter question title...', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder': 'Enter title...', 'class': 'form-control', 'rows': 8})
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    def clean_tags_input(self):
        tags = self.cleaned_data.get('tags_input','')
        return tags.strip()
    def save(self, commit=True):
        question = super().save(commit=False)
        if self.user:
            question.author = self.user.profile
        if commit:
            question.save()
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',') if t.split()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    QuestionTag.objects.get_or_create(question=question, tag=tag)
        return question
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Enter your answer here' ,'class': 'form-control', 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        answer = super().save(commit=False)
        if self.user:
            answer.author = self.user.profile
        if self.question:
            answer.question = self.question
        if commit:
            answer.save()
        return answer