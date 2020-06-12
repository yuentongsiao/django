from learn.models import Note
from django import forms
from django.contrib.auth.models import User
import re

class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'  # __all__为所有字段
        labels = {
            'title': '笔记名称',
            'classes': '笔记类别',
            'tag': '标签',
            'content': '笔记内容',
            'uptime': '上传时间',
            'comment': '评价'
        }
        widgets = {
            'title': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'classes': forms.widgets.Select(attrs={'class': 'form-control'}),
            'tag': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'content': forms.widgets.Textarea(attrs={'class': 'form-control'}),
            'uptime': forms.widgets.DateTimeInput(attrs={'class': 'form-control'}),
            'comment': forms.widgets.TextInput(attrs={'class': 'form-control'})

        }  # 必须按定义的字段顺序排列


class PersonModelForm(forms.ModelForm):
    class Meta:

        fields = '__all__'  # __all__为所有字段
        labels = {
            'p_username': '用户名',
            'p_name': '姓名',
            'p_sex': '性别',
            'p_age': '年龄',
            'p_time': '出生日期',
            'p_phone': '电话',
            'p_email': '邮箱',
            'p_noteClass': '学习方向',
            'p_photo': '照片',
            'p_about': '个人介绍',
        }
        widgets = {
            'p_username': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'p_name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'p_sex': forms.widgets.Select(attrs={'class': 'form-control'}),
            'p_age': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'p_time': forms.widgets.DateTimeInput(attrs={'class': 'form-control'}),
            'p_phone': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'p_email': forms.widgets.EmailInput(attrs={'class': 'form-control'}),
            'p_noteClass': forms.widgets.Select(attrs={'class': 'form-control'}),
            'p_photo': forms.widgets.ClearableFileInput(attrs={'class': 'form-control'}),
            'p_about': forms.widgets.Textarea(attrs={'class': 'form-control'}),
        }  # 必须按定义的字段顺序排列


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='用户名', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='电子邮件',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='再次输入', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise forms.ValidationError("用户名至少3个字节")
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长了")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在")

        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("电子邮箱已经存在了")
        else:
            raise forms.ValidationError("请输入有效的电子邮件")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码过短，最少6位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长，最多20位")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("您输入的两次密码不一致，请重试")

        return password2


#登录
class LoginForm(forms.Form):

    username = forms.CharField(label='用户名', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))  #
    password = forms.CharField(label='密  码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(e1mail__exact=username)
            if not filter_result:
                raise forms.ValidationError("此电子邮件不存在.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("此用户名不存在. 请先注册.")
        return username



#修改密码
class PwdChangeForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='再次输入', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("此电子邮件不存在.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("此用户名不存在. 请先注册.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码过短，最少6位")

        elif len(password1) > 20:
            raise forms.ValidationError("密码过长，最多20位")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("您输入的两次密码不一致，请重试")
        return password2
