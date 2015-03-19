# -*- coding: utf-8 -*-
from django.db import models
from uuidfield import UUIDField


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)


class User(models.Model):
    uuid = UUIDField(auto=True, primary_key=True, hyphenate=True)
    name = models.CharField(max_length=100)
