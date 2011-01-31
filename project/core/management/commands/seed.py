# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import os
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *apps, **options):

        print "OK"