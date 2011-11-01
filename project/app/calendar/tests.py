"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import datetime, timedelta

from django.test import TestCase
from app.calendar.models import Event, RepeatOption
from app.contacts.models import Contact
from core import Core
from core.auth.company.models import Company
from core.auth.group.models import Group
from core.auth.user.models import User


def is_datetimes_same_day(date1,date2):
    return (date1-date2).days == 0

def is_datetime_in_list_of_datetimes(date1,list_of_datetimes):
    for date in list_of_datetimes:
        if is_datetimes_same_day(date1, date):
            return True

    return False

class CalendarTesting(TestCase):
    def setUp(self):

        self.group1 = Group.objects.get_or_create(name="group1")[0]
        company = Company.objects.get_or_create(name="TestFirma", admin_group = self.group1)[0]

        self.user1 = User.objects.get_or_create(username="testbruker", company=company)[0]
        self.user2 = User.objects.get_or_create(username="testbruker2", company=company)[0]
        self.user3 = User.objects.get_or_create(username="testbruker3", company=company)[0]

        Core.set_test_user(self.user1)

        self.contact1 = Contact.objects.get_or_create(name="Customer1")[0]

        self.group1.add_member(self.user2)

    def testRepeatedEventInCalendar(self):
        repeat_option = RepeatOption.objects.get_or_create(available_option="weekly",
                       times=3,
                       repeat_until=datetime.now() + timedelta(days=30)
        )[0]

        event = Event.objects.get_or_create(start=datetime.now(), end=datetime.now()+timedelta(days=2))[0]


        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=21), event.get_dates()), False)
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=22), event.get_dates()), False)
        event.repeat = repeat_option
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=21), event.get_dates()), True)
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=22), event.get_dates()), True)

    def testSpecialCaseInRepeatedEventInCalendar(self):
        repeat_option = RepeatOption.objects.get_or_create(available_option="weekly",
                       times=3,
                       repeat_until=datetime.now() + timedelta(days=30)
        )[0]

        event = Event.objects.get_or_create(start=datetime.now(), end=datetime.now()+timedelta(days=2))[0]
        event.repeat = repeat_option

        #First, we check that the event is active 22 days after, it should, because the event last for 2 days
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=21), event.get_dates()), True)

        #Editing event on date
        special_case_event = Event.objects.get_or_create(start=datetime.now()+timedelta(days=21),
                                            end=datetime.now()+timedelta(days=21)+timedelta(days=0))[0]

        event.special_cases.add(special_case_event)
        
        #But after the special-case edit, it should not longer last a second day..
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=22), event.get_dates()), False)
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=22), event.get_dates()), False)
        self.assertEqual(is_datetime_in_list_of_datetimes(datetime.now()+timedelta(days=21), event.get_dates()), True)
