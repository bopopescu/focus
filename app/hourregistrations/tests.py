import calendar
from datetime import datetime, timedelta, date
from django.test import TestCase
from app.hourregistrations.helpers import generateValidPeriode
from core import Core
from core.models import User
from helpers import validForEdit

class TimeTrackingTesting(TestCase):

    def setUp(self):
        self.user1 = User.objects.get_or_create(username="test")[0]
        self.user2 = User.objects.get_or_create(username="test2")[0]
        self.user3 = User.objects.get_or_create(username="test3")[0]

        Core.set_test_user(self.user3)

    def testgenerateValidPeriode(self):

        todayDate = "1.1.2011"
        now = datetime.strptime(todayDate, "%d.%m.%Y")

        days = calendar.monthrange(now.year,now.month)

        p = generateValidPeriode(today=todayDate)

        self.assertEqual("01.01.2011", p[0])
        self.assertEqual("01.01.2011", p[1])

        self.user3.set_daysIntoNextMonthHourRegistration(3)
        self.user3.save()
        
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2010", p[0])
        self.assertEqual("01.01.2011", p[1])

        todayDate="31.3.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.03.2020", p[0])
        self.assertEqual("31.03.2020", p[1])

        todayDate="1.1.2011"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2010", p[0])
        self.assertEqual("01.01.2011", p[1])

        todayDate="1.3.2005"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2005", p[0])
        self.assertEqual("01.03.2005", p[1])

        todayDate="5.3.2005"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.03.2005", p[0])
        self.assertEqual("05.03.2005", p[1])

        todayDate="3.3.2005"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2005", p[0])
        self.assertEqual("03.03.2005", p[1])

        todayDate="29.2.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2020", p[0])
        self.assertEqual("29.02.2020", p[1])

        todayDate="4.5.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("04.05.2020", p[1])

        todayDate="3.6.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        #Test expiring daysIntoNextMonth on users
        
        self.user3.set_daysIntoNextMonthHourRegistration(3, expireDate = "01.03.2020")

        todayDate="3.6.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.06.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        self.user3.set_daysIntoNextMonthHourRegistration(3, expireDate = "03.06.2020")

        todayDate="3.6.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        self.user3.set_daysIntoNextMonthHourRegistration(3, expireDate = "03.01.2020")

        todayDate="22.12.2019"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2019", p[0])
        self.assertEqual("22.12.2019", p[1])

        todayDate="02.01.2020"
        p = generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2019", p[0])
        self.assertEqual("02.01.2020", p[1])
        

    def testvalidForEdit(self):

        self.assertEqual(validForEdit("1.1.2011", today="1.1.2011"), True)
        self.assertEqual(validForEdit("12.12.2010", today="1.1.2011"), False)
        self.assertEqual(validForEdit("1.5.2011", today="1.6.2011"), False)
        self.assertEqual(validForEdit("12.12.2009", today="1.1.2011"), False)
        self.assertEqual(validForEdit("12.1.2011", today="12.1.2011"), True)
        self.assertEqual(validForEdit("5.10.2005", today="1.1.2011"), False)

        self.user3.set_daysIntoNextMonthHourRegistration(3)
        self.user3.save()

        self.assertEqual(validForEdit("10.11.2011", today="10.11.2011"), True)
        self.assertEqual(validForEdit("12.12.2010", today="11.12.2010"), False)
        self.assertEqual(validForEdit("1.1.2011", today="31.12.2010"), False)
        self.assertEqual(validForEdit("2.12.2010", today="4.1.2011"), False)
        self.assertEqual(validForEdit("2.12.2010", today="3.1.2011"), True)
        self.assertEqual(validForEdit("12.12.2011", today="1.1.2011"), False)
        self.assertEqual(validForEdit("11.2.2011", today="3.3.2011"), True)
        self.assertEqual(validForEdit("31.12.2010", today="28.12.2010"), False)