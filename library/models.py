import uuid

from django.db import models
from django.db.models.functions import Upper
from django.urls import reverse

from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=32)
    objects = models.Manager()
    # books

    def __str__(self):
        return self.name

    def url(self):
        return reverse('lib:genre-list') + f'#g-{self.id}'

    # class Meta:
    #     ordering = ['name']


class Author(models.Model):
    first = models.CharField(max_length=32)
    last = models.CharField(max_length=32, null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    portrait = models.URLField(null=True, blank=True)
    objects = models.Manager()
    # books

    def __str__(self):
        return f'{self.first} {self.last}'

    def url(self):
        return reverse('lib:author-detail', kwargs={
            'pk': self.id
        })

    def genres(self):
        return Genre.objects.filter(books__author__exact=self).distinct()

    def comments(self):
        return Comment.objects.filter(book__author__exact=self)

    class Meta:
        ordering = ['last', 'first']


class Book(models.Model):
    title = models.CharField(max_length=128)
    cover = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    objects = models.Manager()
    # comments
    # instances

    def __str__(self):
        return self.title

    def url(self):
        return reverse('lib:book-detail', args=[self.id])


class Comment(models.Model):
    user = models.CharField(max_length=32)
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created']


class Instance(models.Model):

    STATUSES = [
        ('a', 'Available'),
        ('o', 'On Loan')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, related_name='instances', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUSES, default='a')
    due_back = models.DateField(null=True, blank=True)

    def url(self):
        return reverse('lib:instance-detail', kwargs={
            'pk': self.id
        })

    def is_expired(self):
        return timezone.now().date() > self.due_back
