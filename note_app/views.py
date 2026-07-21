from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import Registerform
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
import markdown
from django.utils.safestring import mark_safe


# Homepage
@login_required(login_url='login')
def homepage(request):
    date = datetime.now()
    time = int(date.strftime('%H'))

    msg = 'Good '
    if time < 12:
        msg += 'morning'
    elif time < 16:
        msg += 'afternoon'
    elif time < 18:
        msg += 'evening'
    else:
        msg += 'night'

    greeting = f'{msg}! {request.user.username}'
    notes = Note.objects.filter(user=request.user, is_deleted=False).order_by('created_at')
    #, is_deleted=False

    context = {
    'greeting': greeting,
    'notes': notes,
}

    return render(request, "homepage.html", context)



# Create Note
# @login_required(login_url='login')
# def create_note(request):

#     if request.method == "POST":

#         title = request.POST.get("title")
#         content = request.POST.get("content")
#         completed = request.POST.get("completed") == "on"

#         note = Note.objects.create(
#          user=request.user,
#          title=title,
#          content=content,
#          completed=completed,
#          color=request.POST.get("color", "default")
# )

#         return redirect("note_detail", note_id=note.id)

#     return render(request, "create_note.html")
@login_required(login_url='login')
def create_note(request):
    if request.method == "POST":
        note = Note.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            attachment=request.FILES.get("attachment"),
        )
        return redirect("note_detail", note_id=note.id)
    return render(request, "create_note.html")


# View Note
@login_required(login_url='login')
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    rendered_content = mark_safe(markdown.markdown(note.content))
    return render(request, "note_detail.html", {"note": note, "rendered_content": rendered_content})


# Edit Note
@login_required(login_url='login')
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()
        return redirect("note_detail", note_id=note.id)
    return render(request, "edit_note.html", {"note": note})


# Delete Note
@login_required(login_url='login')
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.is_deleted = True
        note.save()
        return redirect("homepage")
    return render(request, "delete_note.html", {"note": note})


@login_required(login_url='login')
def trash(request):
    notes = Note.objects.filter(user=request.user, is_deleted=True)
    return render(request, "trash.html", {"notes": notes})


@login_required(login_url='login')
def restore_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_deleted = False
    note.save()
    return redirect("trash")




def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Journals')
        return redirect('homepage')
    
    form = Registerform()
    errors = None

    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created and Login Successful')
                return redirect('homepage')   # was 'home'
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('signup')   # was 'register' — no such name in urls.py

    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'signup.html', context)





def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("homepage")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')