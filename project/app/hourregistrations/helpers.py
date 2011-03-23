from datetime import datetime, timedelta, date
import time
from core import Core
from django.utils.translation import ugettext as _

def calculateHoursWorked(start, end):
    diff = 0

    diff = end - start

    if diff < 1:
        return 0

    diff = str(diff / 3600)

    return diff

def get_month_by_number(id):
    monthNames = [_('January'), _('February'), _('Mars'), _('April'), _('May'), _('June'), _('July'), _('August'),
                    _('September'), _('Oktober'),_('November'), _('Desember')]

    return monthNames[id-1]