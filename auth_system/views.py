from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from auth_system.forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")

    else:
        form = CustomUserCreationForm()
        messages.error(request, "some error")
    return render(
        request,
        template_name="auth_system/register.html",
        context={"form": form}
    )
