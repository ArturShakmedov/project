from django.shortcuts import render, redirect
from .models import Category, Article, Comment, Favourite
from .forms import ArticleForm, LoginForm, RegisterForm, CommentForm
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    articles = Article.objects.all()
    context = {

        'articles': articles,
        'title': 'Главная страница'
    }
    return render(request, 'courses/index.html', context)

class IndexView(ListView):
    model = Article  # По умолчанию выводит ВСЕ объекты этой модели
    template_name = 'courses/index.html'  # по умолчанию ищет article_list.html
    context_object_name = 'articles'  # По умолчанию выводит под именем objects
    extra_context = {
        'title': 'Главная страница'
    }





# 1 - Сделать переключение по страницам категорий
# 2 - Вывести логику категорий в отдельную функцию

def category_view(request, pk): # pk - primary key - id категории

    # Вывести 1 конкретную категорию по ее pk
    category = Category.objects.get(pk=pk)
    # Надо вывести статьи только по определенной категории
    articles = Article.objects.filter(category=category)

    context = {
        'title': f'Категория: {category.title}',
        'articles': articles
    }
    return render(request, 'courses/index.html', context)

class CategoryView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'courses/index.html'

    # Переделать стандартный вывод всех объектов
    def get_queryset(self):  # Где pk?
        return Article.objects.filter(category_id=self.kwargs['pk'])

    # Как динамически поменять заголовок или добавить данные
    def get_context_data(self, *, object_list=None, **kwargs):
        # Надо сохранить контекст который уже есть
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context



# Выводим детали статьи
# Сделаем страницу формы, чтобы пользователь создавал статьи

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)

    context = {
        'article': article
    }
    return render(request, 'courses/article_detail.html', context)


class ArticleDetail(DetailView):  # article_detail.html
    model = Article
    context_object_name = 'article'
    template_name = 'courses/article_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['title'] = f'Статья: {article.title}'
        return context


def save_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Сохраняем но не подтверждаем
            # Потому что нужно дополнить данные
            comment.article = Article.objects.get(pk=pk)
            comment.user = request.user
            comment.save()  # Финальное сохранение
            return redirect('article', pk)




def article_create(request):
    # Работает в 2х режимах
    # GET - показать страницу
    # POST - пользователь отправляет данные а мы их принимаем
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('article', article.pk)

    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'courses/article_form.html', context)

class ArticleCreate(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'courses/article_form.html'
    extra_context = {
        'title': 'Создание новой статьи'
    }


# Изменение статьи
class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'courses/article_form.html'
    extra_context = {
        'title': 'Изменение статьи'
    }

class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


# Изучить как пишутся views на классах
# Реализовать 6 view на классах
# Начать логику входа в аккаунт и регистрацию

# Реализуем логику входа в аккаунт и регистрацию

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Вход в аккаунт'
    }
    return render(request, 'courses/user_form.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        form = RegisterForm()



    context = {
        'form': form,
        'title': 'Регистрация пользователя'
    }
    return render(request, 'courses/user_form.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def profile_view(request, pk):
    user = User.objects.get(pk=pk)
    articles = Article.objects.filter(author=user)
    favs = Favourite.objects.filter(user=user)
    favs = [i.article for i in favs]
    context = {
        'user': user,
        'articles': articles,
        'favs': favs,
        'title': 'Страница пользователя'
    }
    return render(request, 'courses/profile.html', context)


def add_delete_favourite(request, pk):
    article = Article.objects.get(pk=pk)
    user = request.user
    fav = Favourite.objects.filter(article=article, user=user)
    if fav:
        fav2 = Favourite.objects.get(article=article, user=user)
        fav2.delete()
    else:
        Favourite.objects.create(article=article, user=user)
    return redirect('article', pk)




