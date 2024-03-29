from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
               path('books/', views.BookListView.as_view(), name='books'),
               path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

               path('authors/', views.AuthorListView.as_view(), name='authors'),
               path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
               path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
               path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
               path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

               path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
               path('loaned/', views.borrowedListView.as_view(), name='borrowed-author'),
               path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
               path('book/create/', views.BookCreate.as_view(), name='book_create'),
               path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
               path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='delete_update'),
               ]
