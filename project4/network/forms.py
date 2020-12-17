from django import forms
from .models import Post, Follow, Comments


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['likes']