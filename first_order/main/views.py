from django.contrib import messages
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.utils.text import slugify


from django.views.generic import CreateView

from .forms import *


def create_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.title, allow_unicode=True)
            category.save()
    else:
        form = CreateCategoryForm()
    return form


def create_history(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.author = request.user
            history.save()
            form.save()
            return redirect('main_page')
    else:
        form = HistoryForm()
    category_form = create_category(request)
    return render(request, 'histories/create_history.html', {'form': form, 'category_form': category_form})


def main_page(request):
    #cont = CustomUser.objects.all()
    #con = cont[id]
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #user = form.get.objects.latests.filter(id=request.user.id)
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserLoginForm()
    return render(request, 'main/main_page.html', {'form': form})


class Register(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'main/create_user.html'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            #user.username = str(user.username)
            user.slug = str(user.username)
            user.save()
            login(request, user)
            return redirect('main_page')
        else:
            pass
    form = CustomUserCreationForm()
    return render(request, 'main/create_user.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('main_page')


def profile(request, slug):
    model = CustomUser.objects.filter(slug=slug)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES)
        Userr = CustomUser.objects.get(slug=slug)
        if form.is_valid():
            #img = form.cleaned_data['avatar']

            changed_user = form.save(commit=False)
            Userr.username = changed_user.username

            Userr.description = changed_user.description

            Userr.avatar = changed_user.avatar
            changed_user.save()
            Userr.save()
            cont = CustomUser.objects.latest('id').id
            usr = CustomUser.objects.get(id=cont)
            usr.delete()
            #return render(request, 'main/profile.html', {'model': model, 'form': form})
            return redirect('/')
    else:
        form = CustomUserChangeForm()
    return render(request, 'main/profile.html', {'model': model, 'form': form})
