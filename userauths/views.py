from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User

def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()

    #context is used to be able to display the form in the template
    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        #Redirect to home page
        messages.warning(request, "Hey you are already Logged In.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            #First email is from userauths/models.py
            #Second email is local variable
            user = User.objects.get(email=email)

            #Automatically login the user if login email exists.
            #first email and password is from userauths/models.py
            user = authenticate(request, email=email, password=password)

            if user is not None:
                #Login function of django
                login(request, user)
                messages.success(request, "You are logged in.")
                #Redirect to home page
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist. Create an account.")
        except:
            #f is formatted string
            messages.warning(request, f"User with {email} does not exist.")

    return render(request, "userauths/sign-in.html")

def logout_view(request):
    #Request is whoever user is logged in.
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")