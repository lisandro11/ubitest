from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

'''
View for user registration
'''
def signup_view(request):
    if request.method == 'POST':
        #receive data from Form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #Save User in db
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('occurrences:list')
    else:
        #if GET Request, create blank Form for view
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

'''
View for user Login
'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('occurrences:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

'''
View for user Logout 
'''
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('occurrences:list')