from django import forms
from ..models import *

selection = []
categories = Category.objects.all()
for category in categories:
    if category.e_name != 'all':
        selection.append((category.e_name, category.name))
selection2 = []
for category in categories:
    if category.e_name != 'notice' and category.e_name != 'all':
        selection2.append((category.e_name, category.name))
selection = tuple(selection)
selection2 = tuple(selection2)

#여기서 현재 로그인 한 사람의 권한을 확인하는 방법은?

class BoardForm_admin(forms.Form):

    title = forms.CharField(max_length=100, label="게시글 제목")
    contents = forms.CharField(widget=forms.Textarea, label="게시글 내용")
    category = forms.ChoiceField(choices=selection)

class BoardForm(forms.Form):

    title = forms.CharField(max_length=100, label="게시글 제목")
    contents = forms.CharField(widget=forms.Textarea, label="게시글 내용")
    category = forms.ChoiceField(choices=selection2)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
