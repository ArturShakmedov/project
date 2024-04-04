from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', category_view, name='category'),
    # path('article/<int:pk>/', article_detail, name='article'),
    # path('article_create/', article_create, name='article_create'),
    path('', IndexView.as_view(), name='index'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('article_create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', user_logout, name='logout'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('fav/<int:pk>/', add_delete_favourite, name='fav')
]