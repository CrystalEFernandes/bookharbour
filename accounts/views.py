from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

def signup_page(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        password=request.POST.get('password')
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        my_user=User.objects.create_user(username=uname,email=email,password=password,first_name=fname,last_name=lname,)
        my_user.save()
        return redirect('home_page')
    return render(request,'signup.html')

def login_page(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=uname, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email

            referring_url = request.session.get('referring_url', 'book_list')
            request.session.pop('referring_url', None)

            return redirect(referring_url)
        else:
            return HttpResponse('Username incorrect')

    request.session['referring_url'] = request.META.get('HTTP_REFERER', 'book_list')

    return render(request, 'login.html')

