from django import forms
from django.core import validators
from .models import Post, Category

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      widget=forms.Select(attrs={'placeholder': 'Категория', 'style': 'border-radius: 5px;border-width: thin;padding: 5px;'}))
    title = forms.CharField(label='Название', widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Название', 'style': 'border-radius: 5px;border-width: thin;padding: 5px;'}),
                            validators=[validators.MinLengthValidator(8)], error_messages= {
        "min_length": "Слишком короткое название!"
    })
    content = forms.CharField(label='Текст', widget=forms.widgets.Textarea(
        attrs={'placeholder': 'Текст', 'style': 'border-radius: 5px;border-width: thin;padding: 5px;'}),
                              validators=[validators.MinLengthValidator(8)],
                              error_messages= {
        "min_length": "Слишком короткое описание!"
    })
    imgs = forms.FileField(label='Изображения', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'imgs')