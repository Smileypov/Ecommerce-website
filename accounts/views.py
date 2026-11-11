from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .models import User

# We need a custom form because the default UserCreationForm
# targets the default auth.User model, not our custom accounts.User model.
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class CustomUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('store:product_list')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })

def login_view(request):
    """
    Custom login view for regular users.
    """
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('store:product_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        pass

    return render(request, 'accounts/login.html')

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('store:product_list')
