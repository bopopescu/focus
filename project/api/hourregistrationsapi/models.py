from decimal import Decimal
from core.models import PersistentModel
from django.db import models
from datetime import datetime, date

class TimeTrackerManager(models.Manager):
    """
    Only returns active TimeTrackers (running or paused)
    """

    def get_query_set(self):
        return super(TimeTrackerManager, self).get_query_set().filter(active=True).filter(deleted=False)


class TimeTracker(PersistentModel):
    """
    A single timer that can be started, paused, resumed and stopped
    """
    name = models.CharField(max_length=64) # name/short description e.g 'Tickets api work'
    active = models.BooleanField(default=True)

    objects = TimeTrackerManager()

    def start_new(self):
        """
        starts or resumes the timer
        """
        last = self.current_period()
        if (last and last.done) or not last:
            WorkPeriod.objects.create(tracker=self)


    def pause(self):
        """
        pauses the timer
        """
        current = self.current_period()
        if current and not current.done:
            current.stop_and_save()

    def stop_and_save(self, description, order):
        """
        stops the timer and creates an Hourregistration
        """
        self.pause()
        self.active = False
        self.save()
        self.create_hour_reg(description, order)


    def create_hour_reg(self, description, order):
        time_info = self.time_info()
        sec_worked, sec_paused = time_info[:2]
        start_time, end_time = time_info[2:]

        hours_worked = Decimal(sec_worked) / Decimal(3600)
        hours_paused = Decimal(sec_paused) / Decimal(3600)

        time_start = u'%d:%d' % (start_time.hour, start_time.minute)
        time_end = u'%d:%d' % (end_time.hour, end_time.minute)

        from app.hourregistrations.models import HourRegistration
        HourRegistration.objects.create(date=date.today(), order=order, description=description,
                                        hours_worked=hours_worked, pause=hours_paused,
                                        time_start=time_start, time_end=time_end)

    def is_running(self):
        current = self.current_period()
        if current and not current.done:
            return True
        return False


    def current_period(self):
        periods = WorkPeriod.objects.filter(tracker=self).order_by("-id")
        if periods:
            return periods[0]


    def time_info(self):
        """
        returns (seconds_worked, seconds_paused, start_time, end_time)
        start_time and end_time are datetime objects
        """
        periods = WorkPeriod.objects.filter(tracker=self).order_by("id")
        if not periods:
            return 0, 0, -1, -1
        total_worked = periods[0].as_seconds()
        time_start = periods[0].start
        total_paused = 0
        for i in range(1, len(periods)):
            total_worked += periods[i].as_seconds()
            diff = periods[i].start - periods[i - 1].end
            total_paused += ((diff.days * 24 * 3600) + diff.seconds)

        last = periods[len(periods) - 1]
        if self.active:
            time_end = -1
            if last.done:
                pause = (datetime.now() - last.end)
                total_paused += ((pause.days * 24 * 3600) + pause.seconds)
        else:
            time_end = last.end
        return total_worked, total_paused, time_start, time_end


class WorkPeriod(PersistentModel):
    tracker = models.ForeignKey(TimeTracker, related_name='time_periods')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)


    def stop_and_save(self):
        if not self.done:
            self.end = datetime.now()
            self.done = True
            self.save()


    def as_seconds(self):
        if self.end:
            diff = self.end - self.start #timedelta object
        else:
            diff = datetime.now() - self.start
        return (diff.days * 24 * 3600) + diff.seconds
