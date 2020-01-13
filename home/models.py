# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from control.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=500)
    description = models.TextField()
    authors = models.ManyToManyField(User)
    status = models.CharField(max_length=1, default='A')
    created_by = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)
    modified = models.DateTimeField(auto_now=True)

class Commit(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	commit_id = models.CharField(max_length=200)
	commit_title = models.CharField(max_length=300)	

class Review(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
	review_id = models.CharField(max_length=200)	
	reviewer = models.CharField(max_length=100)
	review_time = models.DateTimeField()
	review = models.TextField()
	usefulness = models.CharField(max_length=1)	