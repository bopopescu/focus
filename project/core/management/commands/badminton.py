# -*- coding: utf-8 -*-
import re
from django.core.management.base import BaseCommand
from email.header import decode_header
from urllib import urlopen

class Command(BaseCommand):

    def get_file(self, url):
        f = urlopen(url)
        file = f.read()
        f.close()
        return file

    def handle(self, *args, **kwargs):
        url_prefix = "http://www.cupassist.com/planassist/vis_innbydelse.php?ib_id="
        a = self.get_file(url_prefix+"547")

        a = unicode(a.decode("latin1"))

        print a
