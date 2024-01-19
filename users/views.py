from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                            f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, f'Error creating account!')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    original_username = request.user.username
    if request.method == 'POST':
        u_form = forms.UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Account updated for {request.user.username}!')
            return redirect('profile')
        else:
            messages.error(request, f'Error updating account for {request.user.username}!')
    else:
        u_form = forms.UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'original_username': original_username
    }
    return render(request, 'users/profile.html', context)