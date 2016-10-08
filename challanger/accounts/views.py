from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

from .forms import UserLoginForm, UserRegistrationForm, UserRegistrationForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    print(request.user.is_authenticated())
    title = "Login"
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated())
        if next:
            redirect('next','/test/')
        return redirect("/test/")
    return render(request,"form.html",{"form":form, "title":title})

def register_view(request):
    print(request.user.is_authenticated())
    title = "Register"
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request,new_user)
        return redirect("/policy/")

    context = { 'form':form, 'title':title}
    return render(request,"form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/login/")

@login_required(login_url='/login/')
def test_view(request):
    user = request.user.username
    context = { 'user':user}
    return render(request,"testRedirectionForm.html", context)

#need to work on it
def policy_view(request):
    title = "You have to accept it"
    form = UserRegistrationForm(request.POST or None)
    context = { 'form':form, 'title':title}

    if request.method == "POST":
        if form.is_valid():
            if request.POST['acceptingCheckbox']:
                print("Checkbox is checked!!")
                return redirect('/login/')




        
    return render(request,"policy.html",context)

   
    
