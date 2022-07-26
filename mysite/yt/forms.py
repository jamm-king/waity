from django import forms
from .models import *
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):

    username = forms.CharField(max_length=100, label="USER NAME")
    password = forms.CharField(widget=forms.PasswordInput, label="PASSWORD")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                member = BoardMember.objects.get(username=username)
            except:
                self.add_error('password', '존재하지 않는 ID이거나 비밀번호가 다릅니다')
                return
            if not check_password(password, member.password):
                self.add_error('password', '존재하지 않는 ID이거나 비밀번호가 다릅니다')
            else:
                self.user_id = member.id
                self.user_auth = member.auth

