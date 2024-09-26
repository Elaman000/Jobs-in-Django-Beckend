from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from customuser.models import CustomUser
from django.contrib.auth.models import User


from .models import *


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'placeholder': 'Что думаете?'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        }

class SettingsProfileFormActive(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','photo','email','telegram','applicant']
        widgets = {}

# class SettingsProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name','email','name_activity','activity','photo','birth_date','gender','nationality','telegram','whatsapp','phone','web_url','applicant']
#         widgets = {}

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # fields = [
        #     'name_activity','description','name_activity','address', 
        #     'birth_date', 'gender', 
        #     'nationality','team','number_persons','web_url', 'whatsapp',
        # ]
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['user_permissions', 'groups','is_superuser','is_staff','is_active','password','date_joined', 'last_login','username', 'first_name', 'last_name','photo','email','telegram','applicant']

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields= '__all__'


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", 'description', 'logo', 'contact', 'address']
        widgets = {
            # 'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            }
        exclude = ['owner']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['company',"title", 'title_info','content','wage', 'experience', 'schedule',  'number_persons', 'city','area',]
        # widgets = {
        #     'city': forms.Select(attrs={'empty_label': 'Выберите город'}),
        #     'area': forms.Select(attrs={'empty_label': 'Выберите район'}),
        # }
        exclude = ['user']  # Исключаем поле user из формы

    # def clean_title(self):
    #     title = self.cleaned_data["title"]
    #     if len(title) > 200:
    #         raise ValueError("Длина превышает 200 символов.")
    #     return title


class LogRegisterUserForm(UserCreationForm):

    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={
        "class":'form-control',
        'id':'floatingInput',
        'placeholder':'name@example.com',
        'type':'text'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={
        "class":'form-control',
        'id':'exampleFormControlInput1',
        'placeholder':'name@example.com',
        'type':'email'}))
    password1 = forms.CharField(label="Пороль", widget=forms.TextInput(attrs={
        "class":'form-control',
        'id':'exampleInputPassword1',
        'placeholder':'Password',
        'type':'password'}))
    password2 = forms.CharField(label="Повтор пороль", widget=forms.TextInput(attrs={
        "class":'form-control',
        'placeholder':'Password',
        'id':'exampleInputPassword2',
        'type':'password'}))

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']

class LogInForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={
        "class":'form-control',
        'id':'floatingInput',
        'placeholder':'name@example.com',
        'type':'text'}))
    password = forms.CharField(label="Пороль", widget=forms.TextInput(attrs={
        "class":'form-control',
        'id':'exampleInputPassword1',
        'placeholder':'Password',
        'type':'password'}))

    class Meta:
        model = CustomUser
        fields = ['username','password']



# Для редактировани ваканисию
class JobListingForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['title', 'title_info', 'content', 'wage', 'experience', 'schedule', 'number_persons','published']  # Замените на ваши поля

        # fields = [
        #     'title', 'title_info', 'content',
        #     'city', 'area', 'wage', 'user', 'company',
        #     'experience', 'schedule', 'number_persons','published'
        # ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# Для редактировани Компвни
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'description', 'logo', 'address', 'private',
            'activity', 'own', 'contact', 'telegram', 'web_url', 'whatsapp',
            'phone'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }