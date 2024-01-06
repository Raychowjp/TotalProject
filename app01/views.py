from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django import forms
from app01 import models
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"})
    )
    password = forms.CharField(
        label="<PASSWORD>",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "输入密码"})
    )


# Create your views here.
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html', {"form":  form})
    form = LoginForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        user_object = models.UserInfo.objects.filter(username=form.cleaned_data['username'],password = form.cleaned_data['password']).first()
        if user_object:
            return HttpResponse('成功')
        else:
            return render(request, 'login.html', {"form": form, "error":"用户名或密码错误"})
    else:
        return render(request, 'login.html', {"form": form})