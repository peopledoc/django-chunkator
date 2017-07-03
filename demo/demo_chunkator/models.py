# -*- coding: utf-8 -*-
import uuid
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    class Meta:
        ordering = ['title']


class Cover(models.Model):
    book = models.OneToOneField(Book, primary_key=True)
    code = models.CharField(max_length=20)


class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    avatar = models.CharField(max_length=100)
