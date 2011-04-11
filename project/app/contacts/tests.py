"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from app.contacts.models import Contact
from core import Core
from core.auth.company.models import Company
from core.auth.group.models import Group
from core.auth.user.models import User

class ContactsTesting(TestCase):
    def setUp(self):

        self.group1 = Group.objects.get_or_create(name="group1")[0]
        company = Company.objects.get_or_create(name="TestFirma", adminGroup = self.group1)[0]
     
        self.user1 = User.objects.get_or_create(username="testbruker", company=company)[0]
        self.user2 = User.objects.get_or_create(username="testbruker2", company=company)[0]
        self.user3 = User.objects.get_or_create(username="testbruker3", company=company)[0]

        Core.set_test_user(self.user1)

        self.contact1 = Contact.objects.get_or_create(full_name="Customer1")[0]

        self.group1.add_member(self.user2)

    def testUserPerm(self):

        #User1 should be permitted, because user1 is the owner
        self.assertEqual(self.user1.has_permission_to("EDIT", self.contact1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.contact1), True)

        #User2 should get the permission, because user2 is member of group1, who is the adminGroup of the company
        self.assertEqual(self.user2.has_permission_to("EDIT", self.contact1), True)
        self.assertEqual(self.user2.has_permission_to("DELETE", self.contact1), True)

        #But User3 should not have any permission
        self.assertEqual(self.user3.has_permission_to("EDIT", self.contact1), False)
        self.assertEqual(self.user3.has_permission_to("DELETE", self.contact1), False)