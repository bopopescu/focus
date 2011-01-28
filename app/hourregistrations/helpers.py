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

def generateValidPeriode(*args, **kwargs):

    now = datetime.now()

    if 'today' in kwargs:
        now = datetime.strptime(kwargs['today'], "%d.%m.%Y")

    daysIntoNextMonthTimetracking = Core.current_user().get_daysIntoNextMonthHourRegistration(**kwargs)

    #If true, user can still edit last month
    if daysIntoNextMonthTimetracking >= now.day:

        #If January, the user should be able to edit December last year
        if now.month == 1:
            from_date = date(now.year-1, 12, 1)
            to_date = date(now.year, 1, now.day)

        #If rest of the year, set last month editable
        else:
            from_date = date(now.year, now.month-1, 1)
            to_date = date(now.year, now.month, now.day)

    #Else, the user can edit from first this month -> today
    else:
        from_date = date(now.year, now.month, 1)
        to_date = date(now.year, now.month, now.day)

    fromDate = from_date.strftime("%d.%m.%Y")

    if Core.current_user().get_validEditBackToDate(**kwargs):
        fromDate = Core.current_user().validEditBackToDate.strftime("%d.%m.%Y")

    return [fromDate, to_date.strftime("%d.%m.%Y")]

def validForEdit(date, *args,**kwargs):

    now = datetime.now()
    periode = generateValidPeriode(*args, **kwargs)

    if 'today' in kwargs:
        now = datetime.strptime(kwargs['today'], "%d.%m.%Y")
        periode = generateValidPeriode(today=kwargs['today'])

    date = time.mktime(time.strptime("%s"%(date),"%d.%m.%Y"))
    from_date = time.mktime(time.strptime("%s"%(periode[0]),"%d.%m.%Y"))
    to_date = time.mktime(time.strptime("%s"%(periode[1]),"%d.%m.%Y"))


    if date >= from_date and date <= to_date:
        return True

    return False
