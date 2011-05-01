from django.db import models
from django.shortcuts import redirect
from core import Core

class PersistentManager(models.Manager):
    def get_query_set(self):
        return super(PersistentManager, self).get_query_set().filter(deleted=False)

    def filter_current_company(self):

        #Check if no current_user
        if not Core.current_user():
            return None
        
        return super(PersistentManager, self).get_query_set().filter(deleted=False,
                                                                     company=Core.current_user().get_company())