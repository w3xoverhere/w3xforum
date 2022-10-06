from django import forms
from django.core import validators
from .models import Post, Category

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    title = forms.CharField(label='Название', validators=[validators.MinLengthValidator(8)], error_messages= {
        "min_length": "Слишком короткое название!"
    })
    content = forms.CharField(label='Текст', widget=forms.widgets.Textarea(), validators=[validators.MinLengthValidator(8)], error_messages= {
        "min_length": "Слишком короткое описание!"
    })
    imgs = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'imgs')