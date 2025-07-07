from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

@login_required
def edit_profile(request):
    user = request.user
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
        elif form_type == 'password':
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Password change failed. Please check the form.")
            return redirect('edit_profile')

    return render(request, 'terminal/edit_profile.html', {
        'password_form': password_form
    })