from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
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


def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {"queryset": queryset})


class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['title', 'count']

def add_depart(request):
    if request.method == "GET":
        form = DepartModelForm()
        return render(request,"add_depart.html", {"form": form})

    form = DepartModelForm(data= request.POST)
    if form.is_valid():
        form.save()
        return redirect('/depart/list/')
    else:
        return render(request,"add_depart.html", {"form": form})


def delete_depart(request):
    did = request.GET.get('did')
    models.Department.objects.all().filter(id=did).delete()
    return redirect('/depart/list/')


def edit_depart(request):
    if request.method == "GET":
        did = request.POST.get('did')
        object = models.Department.objects.all().filter(id=did).first()
        form = DepartModelForm(instance=object)
        return render(request, 'edit_depart.html', {"form":form})
    did = request.GET.get('did')
    object = models.Department.objects.all().filter(id=did).first()
    form = DepartModelForm(data=request.POST, instance=object)
    if form.is_valid():
        object.save()
        return redirect('/depart/list/')
    else:
        return render(request,"edit_depart.html", {"form":form})

