from django import forms
from .models import Post, Category, Author



class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label='Выберите автора', label='Автор')
    pcategory = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    title = forms.CharField (min_length=24)

    class Meta:
        model = Post
        fields = [
            'author',
            'pcategory',
            'title',
            'text',
           ]