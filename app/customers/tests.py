"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from models import *

class CustomerTesting(TestCase):
    def setUp(self):
        Customer.objects.create(full_name="dfgj", zip=1234)
        User.objects.create_user('test', 'test@example.com', 'test')
        User.objects.create_user('test2', 'test@example.com', 'test')
        Group.objects.create(name="fiogjdf")
   