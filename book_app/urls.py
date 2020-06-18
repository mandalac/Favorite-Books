from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
    path('add_book', views.create_book),
    path('add_to_favorites/<int:book_id>', views.add_to_favorites),
    path('books/edit/<int:book_id>', views.view_edit_page),
    path('edit/<int:book_id>', views.update_book),
    path('delete/<int:book_id>', views.delete),
    path('books/view/<int:book_id>', views.view_page),
    path('un_favorite/<int:book_id>', views.unFavorite),
]