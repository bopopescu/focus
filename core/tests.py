from . import Core
import time
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.contrib.flatpages.models import *

from models import *
from app.customers.models import *

"""
Tests for core

class PermissionsTesting(TestCase):


    def setUp(self):
        FlatPage.objects.create(title="dfgj")
        creator = User.objects.get(username="testgdfg")
        Membership.objects.create(name="fiogjdf")

    def testuserPerm(self):
        user = User.objects.get(username="test")
        page = FlatPage.objects.get(title="dfgj")
        user2 = User.objects.get(username="test2")

        #Test permission on flatpages, before permisisons added
        self.assertFalse(user.has_perm('delete', page))
        self.assertFalse(user.has_perm('view', page))

        ct = ContentType.objects.get_for_model(page)
        Permission.objects.create(user=user, can_view=True,
                                        content_type=ct, object_id=page.id)

        #Test permission on flatpages, after created
        self.assertFalse(user.has_perm('delete', page))
        self.assertTrue(user.has_perm('view', page))

        #Check if another us don't got the permissions..
        self.assertFalse(user2.has_perm('delete', page))
        self.assertFalse(user2.has_perm('view', page))

    def testUserInMembershipPermissions(self):
        membership_obj = Membership.objects.get(name="fiogjdf")
        user = User.objects.all().get(username="testgdfg")
        user2 = User.objects.all().get(username="testgdfg")
        page = FlatPage.objects.get(title="dfgj")

        #Test permission on flatpages, before permisisons added
        self.assertFalse(user.has_perm('delete', page))
        self.assertFalse(user.has_perm('view', page))

        ct = ContentType.objects.get_for_model(page)
        Permission.objects.create(membership = membership_obj, can_view=True,
                                        can_change=True, can_delete=False,
                                        content_type=ct, object_id=page.id)

        user.memberships.add(membership_obj)

        #Check if user got the memberships permissions
        self.assertFalse(user.has_perm('delete', page))
        self.assertTrue(user.has_perm('view', page))

        #Check if another us don't got the permissions..
        self.assertFalse(user2.has_perm('delete', page))
        self.assertFalse(user2.has_perm('view', page))
"""