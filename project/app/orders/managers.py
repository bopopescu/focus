from django.db import models
from django.shortcuts import redirect
from core import Core

class OrderManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(deleted=False, archived=False)

    def filter_current_company(self):
        #Check if no current_user
        if not Core.current_user():
            return None

        return super(OrderManager, self).get_query_set().filter(company=Core.current_user().get_company())


class OrderArchivedManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(deleted=False, archived=True)