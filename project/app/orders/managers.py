from django.db import models
from django.shortcuts import redirect
from core import Core

class OrderManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(deleted=False, archived=False)

class OrderArchivedManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(deleted=False, archived=True)