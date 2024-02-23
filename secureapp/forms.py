from django import forms
from .models import Notice, Comment
'''
class EditForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('notice_title','description', 'pub_date')
'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commenttext']