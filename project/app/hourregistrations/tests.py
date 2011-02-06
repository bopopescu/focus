import calendar
from datetime import datetime, timedelta, date
from django.test import TestCase
from app.customers.models import Customer
from app.hourregistrations.models import HourRegistration, TypeOfHourRegistration
from app.orders.models import Order
from core import Core
from core.models import User
from core.tests import FocusTest

class TimeTrackingTesting(FocusTest):
    def testValidPeriod(self):
        user = self.user3

        user.company.setDaysIntoNextMonthHourRegistration(0)

        todayDate = "1.1.2011"
        p = user.generateValidPeriode(today=todayDate)

        self.assertEqual("01.01.2011", p[0])
        self.assertEqual("01.01.2011", p[1])

        user.company.setDaysIntoNextMonthHourRegistration(3)

        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2010", p[0])
        self.assertEqual("01.01.2011", p[1])

        todayDate = "31.3.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.03.2020", p[0])
        self.assertEqual("31.03.2020", p[1])

        todayDate = "1.1.2011"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2010", p[0])
        self.assertEqual("01.01.2011", p[1])

        todayDate = "1.3.2005"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2005", p[0])
        self.assertEqual("01.03.2005", p[1])

        todayDate = "5.3.2005"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.03.2005", p[0])
        self.assertEqual("05.03.2005", p[1])

        todayDate = "3.3.2005"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2005", p[0])
        self.assertEqual("03.03.2005", p[1])

        todayDate = "29.2.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.02.2020", p[0])
        self.assertEqual("29.02.2020", p[1])

        todayDate = "4.5.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("04.05.2020", p[1])

        todayDate = "3.6.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        #Test expiring daysIntoNextMonth on users

        user.company.setDaysIntoNextMonthHourRegistration(0)

        todayDate = "3.6.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.06.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        user.company.setDaysIntoNextMonthHourRegistration(3)

        todayDate = "3.6.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.05.2020", p[0])
        self.assertEqual("03.06.2020", p[1])

        user.company.setDaysIntoNextMonthHourRegistration(3)

        todayDate = "22.12.2019"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2019", p[0])
        self.assertEqual("22.12.2019", p[1])

        todayDate = "02.01.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.12.2019", p[0])
        self.assertEqual("02.01.2020", p[1])

        user.company.setDaysIntoNextMonthHourRegistration(5)

        todayDate = "08.01.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.01.2020", p[0])
        self.assertEqual("08.01.2020", p[1])

        user.setValidPeriodManually(fromDate="01.01.2010")

        todayDate = "03.01.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.01.2010", p[0])
        self.assertEqual("03.01.2020", p[1])

        user.setValidPeriodManually(fromDate="", toDate="01.01.2030")

        todayDate = "08.01.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.01.2020", p[0])
        self.assertEqual("01.01.2030", p[1])

        user.setValidPeriodManually(fromDate="", toDate="")

        todayDate = "08.01.2020"
        p = user.generateValidPeriode(today=todayDate)
        self.assertEqual("01.01.2020", p[0])
        self.assertEqual("08.01.2020", p[1])

    def testSavedHoursAndUsedOfSaved(self):
        user = self.user3
        todayDate = "1.1.2011"
        now = datetime.strptime(todayDate, "%d.%m.%Y")

        testTypeHour = TypeOfHourRegistration.objects.create(name="Arbeid", description="test")
        testCustomer = Customer.objects.create(cid="10432", full_name="testKunde", email="test@test.com")
        testOrder = Order.objects.create(oid="2342", order_name="test", customer=testCustomer, state="Offer")
        hourRegistration = HourRegistration.objects.create(date=now,
                                                           order=testOrder,
                                                           typeOfWork=testTypeHour,
                                                           time_start="15:00",
                                                           time_end="16:00",
                                                           description="testTime",
                                                           pause="0",
                                                           )

        user.setValidPeriodManually(fromDate="", toDate="")

        #check if user can edit
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), True)

        todayDate = "1.1.2009"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), False)
        todayDate = "1.2.2011"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), True)
        todayDate = "3.2.2011"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), True)
        todayDate = "4.2.2011"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), False)
        todayDate = "4.1.2020"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), False)
        todayDate = "31.12.2010"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), False)

        user.setValidPeriodManually(fromDate="01.01.2000", toDate="01.01.2030")
        todayDate = "4.1.2020"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), True)
        todayDate = "4.1.2000"
        self.assertEqual(user.canEditHourRegistration(hourRegistration, today=todayDate), True)