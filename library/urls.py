from django.urls import path
from . import views

app_name = 'lib'

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name='home'),
    # path("books/", views.book_list, name='book-list'),
    path("book/list/", views.BookListView.as_view(), name='book-list'),
    path("author/list", views.AuthorListView.as_view(), name='author-list'),
    path("genre/list", views.GenreListView.as_view(), name='genre-list'),
    path("book/<int:pk>", views.book_detail, name='book-detail'),
    path("author/<int:pk>", views.author_detail, name='author-detail'),
    path("comment/<int:pk>/add", views.add_comment, name='add-comment'),
    path("instance/<uuid:pk>", views.instance_detail, name='instance-detail'),
    path("lend/instance/<uuid:pk>/", views.lend_instance, name='lend-instance'),
    path("return/instance/<uuid:pk>/", views.return_instance, name='return-instance'),
]
