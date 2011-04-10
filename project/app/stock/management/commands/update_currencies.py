# -*- coding: utf-8 -*-
import csv
import urllib
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from core.mail import send_mail

def getClass(app, model):
    content_type = ContentType.objects.get(app_label=app, model=model)
    model = content_type.model_class()
    return model

Currency = getClass("stock", "currency")

class Command(BaseCommand):
    def handle(self, *apps, **options):
        try:
            csv_file = "https://www.dnbnor.no/portalfront/datafiles/miscellaneous/csv/kursliste.csv"

            val_file = csv.reader(urllib.urlopen((csv_file)))
            values = [val.iso for val in Currency.objects.all()]

            for i in val_file:
                iso = i[2]
                if i[9]:
                    value = Decimal(i[9])
                    if i[1]:
                        innok = Decimal(i[1])
                        if iso in values:
                            currency = Currency.objects.get(iso=iso)
                            currency.value = value / innok
                            currency.save()
        except Exception, e:
            send_mail("Problems during currency update", "%s" % e, "no-reply@focustime.no", ["fredrik@fncit.no"],
                      fail_silently=False)