from django.test import TestCase
from django.contrib.flatpages.models import *
from models import *
from app.customers.models import *
from . import Core

class PermissionsTesting(TestCase):

    def testuserPerm(self):
        customer1 = Customer.objects.get_or_create(full_name="Customer1",cid=1)
        customer2 = Customer.objects.get_or_create(full_name="Customer2",cid=2)
        customer3 = Customer.objects.get_or_create(full_name="Customer3",cid=3)
        user1 = User.objects.get_or_create(username="test")
        user2 = User.objects.get_or_create(username="test2")
        user3 = User.objects.get_or_create(username="test3")
        group1 = Group.objects.get_or_create(name="group1")
        group2 = Group.objects.get_or_create(name="group2")
        group3 = Group.objects.get_or_create(name="group3")
        role1 = Role.objects.get_or_create(name="Leader")

        #user1[0].grant_permissions("EDIT", customer1[0])
        user1[0].grant_role("Member", customer1[0])
        user1[0].grant_role("Leader", customer1[0])

        Role.objects.get(name="Member").grant_actions("DELETE")

        self.assertTrue(user1[0].has_permission_to("EDIT", customer1[0]))
        self.assertTrue(user1[0].has_permission_to("DELETE", customer1[0]))

        #Test permission on flatpages, before permisisons added
        #self.assertFalse(user.has_perm('delete', page))
        #self.assertFalse(user.has_perm('view', page))