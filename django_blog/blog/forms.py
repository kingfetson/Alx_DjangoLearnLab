from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget  # Add this import
from .models import Post, Profile, Comment

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
        """
        Custom validation for title
        """
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        """
        Custom validation for content
        """
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content
    
    def clean_tags(self):
        """
        Custom validation for tags
        """
        tags = self.cleaned_data.get('tags')
        if tags:
            # Convert tags to string and validate
            tags_str = str(tags)
            if len(tags_str) > 200:
                raise forms.ValidationError('Tags are too long. Please use fewer tags or shorter tag names.')
        return tags


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments
    """
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
        labels = {
            'content': ''
        }
    
    def clean_content(self):
        """
        Custom validation for comment content
        """
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Comment cannot be empty.')
        if len(content) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        return content.strip()


class ReplyForm(forms.ModelForm):
    """
    Form for replying to comments
    """
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
        labels = {
            'content': ''
        }
    
    def clean_content(self):
        """
        Custom validation for reply content
        """
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Reply cannot be empty.')
        if len(content) < 3:
            raise forms.ValidationError('Reply must be at least 3 characters long.')
        if len(content) > 1000:
            raise forms.ValidationError('Reply cannot exceed 1000 characters.')
        return content.strip()


class SearchForm(forms.Form):
    """
    Form for searching posts
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Search posts by title, content, or tags...'
        })
    )
    
    def clean_query(self):
        query = self.cleaned_data.get('query', '').strip()
        if query and len(query) < 2:
            raise forms.ValidationError('Search query must be at least 2 characters long.')
        return query


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional fields
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    """
    Form for editing user profile
    """
    password = None  # Remove password field from the form
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }