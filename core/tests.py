from . import Core
import time
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.contrib.flatpages.models import *

from models import *
from app.customers.models import *

class PermissionsTesting(TestCase):


    def setUp(self):
        customer1 = Customer.objects.create(full_name="Customer1")
        customer2 = Customer.objects.create(full_name="Customer2")
        customer3 = Customer.objects.create(full_name="Customer3")
        user1  = User.objects.get(username="test")
        user2  = User.objects.get(username="test2")
        user3  = User.objects.get(username="test3")
        group1 = Group.objects.create(name="group1")
        group2 = Group.objects.create(name="group2")
        group3 = Group.objects.create(name="group3")

    def testuserPerm(self):
        user = User.objects.get(username="test")
        page = FlatPage.objects.get(title="dfgj")
        user2 = User.objects.get(username="test2")

        #Test permission on flatpages, before permisisons added
        self.assertFalse(user.has_perm('delete', page))
        self.assertFalse(user.has_perm('view', page))