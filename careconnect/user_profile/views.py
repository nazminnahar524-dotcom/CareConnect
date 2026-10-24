import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required(login_url='login')
def my_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Account Delete Handling
        if 'delete_account' in request.POST:
            if profile.profile_photo and os.path.isfile(profile.profile_photo.path):
                try:
                    os.remove(profile.profile_photo.path)
                except Exception:
                    pass
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('login')

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            # Check if user clicked the "Remove Photo" checkbox
            if 'remove_photo' in request.POST:
                if profile.profile_photo and os.path.isfile(profile.profile_photo.path):
                    try:
                        os.remove(profile.profile_photo.path)
                    except Exception:
                        pass
                profile.profile_photo = None
                profile.save()
            # Check if a new photo is uploaded, delete old one from storage
            elif 'profile_photo' in request.FILES:
                if profile.profile_photo and os.path.isfile(profile.profile_photo.path):
                    try:
                        os.remove(profile.profile_photo.path)
                    except Exception:
                        pass

            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('my_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user_profile/my_profile.html', context)