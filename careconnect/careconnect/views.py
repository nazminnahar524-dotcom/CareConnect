from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home_view(request):
    return render(request, 'home.html')
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # রেজিস্ট্রেশন সফল হলে লগইন পেজে পাঠিয়ে দেবে
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})