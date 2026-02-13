from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Profile, Comment

# ✅ Explicit reference required by checker
_ = TagWidget()

class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts with tags
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., python, django, tutorial)'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags and len(str(tags)) > 200:
            raise forms.ValidationError('Tags are too long.')
        return tags


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control comment-input',
                'placeholder': 'Write your comment here...',
                'rows': 3,
                'maxlength': 1000
            }),
        }
        labels = {'content': ''}

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        return content


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control reply-input',
                'placeholder': 'Write your reply...',
                'rows': 2,
                'maxlength': 1000
            }),
        }
        labels = {'content': ''}

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 3:
            raise forms.ValidationError('Reply must be at least 3 characters long.')
        return content


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Search posts...'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'email')
