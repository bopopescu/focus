from django.db import models
from core import Core

class PersistentManager(models.Manager):
    def get_query_set(self):
        return super(PersistentManager, self).get_query_set().filter(deleted=False)

    def filter_current_company(self):
        return super(PersistentManager, self).get_query_set().filter(deleted=False, company = Core.current_user().get_company())