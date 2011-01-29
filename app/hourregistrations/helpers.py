from datetime import datetime, timedelta, date
import time
from core import Core

def calculateHoursWorked(start, end):
    diff = 0

    diff = end - start

    if diff < 1:
        return 0

    diff = str(diff / 3600)

    return diff