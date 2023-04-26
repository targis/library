from django.db.models import Count, Prefetch
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Book, Author, Genre, Comment, Instance


def home(request):
    return render(request, template_name='library/index.html',
                  context={
                      'books_count': Book.objects.count(),
                      'authors_count': Author.objects.count(),
                      'genres_count': Genre.objects.count(),
                  })


def book_list(request):
    return render(request, template_name='library/book-list.html',
                  context={
                      'books': Book.objects.order_by('title').annotate(comments_count=Count('comments')).all(),
                  })


def author_list(request):
    return render(request, template_name='library/author-list.html',
                  context={
                      'authors': Author.objects.order_by('last', 'first') \
                  .annotate(books_count=Count('books'), comments_count=Count('books__comments')).all(),
                  })


def genre_list(request):
    # return render(request, template_name='library/genre-list.html',
    #               context={
    #                   'genres': Genre.objects.order_by('name').prefetch_related('books', 'books__author').all(),
    #               })
    return render(request, template_name='library/genre-list.html',
                  context={
                      'genres': Genre.objects.order_by(Lower('name')).prefetch_related('books__author').all(),
                  })


def book_detail(request, pk):
    return render(request, template_name='library/book-detail.html',
                  context={
                      'book': Book.objects.select_related('author').prefetch_related(
                          'genres', 'instances', 'comments'
                      ).get(id__exact=pk),
                  })


def author_detail(request, pk):
    return render(request, template_name='library/author-detail.html',
                  context={
                      'author': Author.objects.get(id__exact=pk),
                      'comments': Comment.objects.filter(book__author__id__exact=pk).select_related('book'),
                      'genres': Genre.objects.filter(books__author__exact=pk),
                      'books': Book.objects.filter(author__exact=pk),
                  })


def add_comment(request, pk):
    book = Book.objects.get(pk=pk)
    print(request.POST)
    user = request.POST.get('user')
    text = request.POST.get('text')
    if user and text:
        Comment.objects.create(
            user=user,
            text=text,
            book=book
        )
    return HttpResponseRedirect(book.url())


def instance_detail(request, pk):
    return render(request, template_name='library/instance-detail.html',
                  context={
                      'instance': Instance.objects.get(id__exact=pk),
                  })


def lend_instance(request, pk):
    due_back = request.POST.get('due_back')
    instance = Instance.objects.get(id__exact=pk)
    print(due_back)
    if due_back:
        instance.due_back = due_back
        instance.status = 'o'
        instance.save()
    return HttpResponseRedirect(instance.book.url())


def return_instance(request, pk):
    inst = Instance.objects.get(pk=pk)
    inst.due_back = None
    inst.status = 'a'
    inst.save()
    return HttpResponseRedirect(inst.book.url())
