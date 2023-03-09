from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView
from .forms import *
from .models import *


# данная функция собирает все объекты класса History если нет заданного слова для поиска, а если оно есть, то оно выводит все посты у которых категория или название похоже на введённое слово
@login_required
def histories(request):
    search_query = request.GET.get('q')
    if search_query:
        history = History.objects.filter(title__icontains=search_query)
        hist = History.objects.filter(category__title__icontains=search_query)
        paginator = Paginator(history | hist, 1)
    else:
        paginator = Paginator(History.objects.all(), 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'history': page_object,
    }
    return render(request, 'histories/history_page.html', context)


# функция для создания категории
def create_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            # slug категории соответствует названию категории
            category.slug = slugify(category.title, allow_unicode=True)
            category.save()
    else:
        form = CreateCategoryForm()
    return form


# функция для создания истории и если пользователь на найдёт нужной ему категории, то он сможет создать её в modal
def create_history(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.author = request.user
            history.save()
            form.save()
            return redirect('/')
    else:
        form = HistoryForm()
    category_form = create_category(request)
    return render(request, 'histories/create_history.html', {'form': form, 'category_form': category_form})


# на главной странице пользователь может войти в свой аккаунт, введя данные в всплывающую modal
def main_page(request, text=None):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserLoginForm()
    return render(request, 'main/main_page.html', {'form': form, 'text': text})


# регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
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
    return redirect('/')


# данная функция вызывается когда пользователь повышает уровень и вывод результат
def is_showing(request):
    text = False
    return main_page(request, text)


# данная функция даёт возможность посмотреть профиль указанного пользователя
def profile(request, slug):
    model = CustomUser.objects.filter(slug=slug)
    profile_owner = CustomUser.objects.get(slug=slug)
    history = History.objects.filter(author=profile_owner)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES)
        if form.is_valid():
            # скорее всего данная реализация не совсем верна, но  я создаю нового пользователя с изменёнными значениями, а потом присваиваю их текущему пользователю и удаляю промежуточного юзера (эта часть нужна для возможности изменения профиля пользователя через modal в профиле
            changed_user = form.save(commit=False)
            profile_owner.username = changed_user.username

            profile_owner.description = changed_user.description

            profile_owner.avatar = changed_user.avatar
            changed_user.save()
            profile_owner.save()
            cont = CustomUser.objects.latest('id').id
            usr = CustomUser.objects.get(id=cont)
            usr.delete()
            return redirect('/')
    else:
        form = CustomUserChangeForm()
    paginator = Paginator(history, 1)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'main/profile.html', {'model': model, 'form': form, 'history': page_object, 'profile_owner': profile_owner})


# изменение профиля пользователя
def edit_profile(request, slug):
    user = CustomUser.objects.get(slug=slug)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES)
        if form.is_valid():
            # если введённые данные коректны, то я создаю промежуточного пользователя и присваиваю основному пользователю значения промежутчного пользователя, промежуточный пользователь удаляется
            userr = form.save(commit=False)
            user.username = userr.username
            user.avatar = userr.avatar
            user.status = userr.status
            user.save()
            redirect('/')
    else:
        form = CustomUserChangeForm()
    return render(request, 'main/edit_profile.html', {'form': form})


# эта функция поднимает уровень пользователя до уровня level (level - число которое нужно присвоить пользователю)
def up_level(request, slug, level):
    user = CustomUser.objects.get(slug=slug)
    user.level = level
    if user.level > 3:
        user.level = 3
        text = False
        return main_page(request, text)
    else:
        user.save()
        text = 'Уровень успешно повышен'
        return main_page(request, text)


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'main/change_password.html'
    success_url = reverse_lazy('main_page')


# нахождение категорий по заданному слову
def histories_with_filter(request, pk):
    paginator = Paginator(History.objects.filter(category_id=pk), 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'histories/history_page.html', {'history': page_object})
