from piston.handler import BaseHandler
from piston.utils import rc
from api.hourregistrationsapi.forms import TimeTrackerForm
from api.hourregistrationsapi.models import TimeTracker
from app.hourregistrations.models import HourRegistration
from core import Core

class HourRegistrationHandler(BaseHandler):
    model = HourRegistration
    allowed_methods = ('GET', 'PUT', 'POST')
    fields = ('date', ('order', ('id', 'order_name')), 'time_start', 'time_end', 'description',
              'pause', 'hours_worked', )


    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", HourRegistration).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except HourRegistration.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request):
        pass

    def update(self, request, id):
        pass



class TimeTrackerHandler(BaseHandler):
    model = TimeTracker
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    fields = ('id', 'name', 'active', 'time_info', ('time_periods', ('start', 'end', 'done',),),)


    @classmethod
    def time_info(cls, time_tracker):
        return time_tracker.time_info()


    def read(self, request, id=None):
        #all = Core.current_user().get_permitted_objects("VIEW", TimeTracker).filter(trashed=False).filter(active=True)
        all = TimeTracker.objects.all() #testing
        if id:
            try:
                return all.get(id=id)
            except TimeTracker.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request):
        form = TimeTrackerForm(request.POST, instance=TimeTracker())
        if form.is_valid():
            tracker = form.save()
            return tracker
        else:
            return form.errors


    _update_actions = {
        'stop': lambda tracker: tracker.stop_and_save(),
        'start': lambda tracker: tracker.start_new(),
        'pause': lambda tracker: tracker.pause()
    }
    def update(self, request, id=None):
        action = request.PUT.get('action', False)
        print self._update_actions
        if action not in self._update_actions:
            return rc.BAD_REQUEST
        if id:
            self._update_instance(action, id)
        else:
            self._update_all(action)
        return {'success': True}


    def _update_instance(self, action, id):
        """
        Updates a single timer
        """
        print "updating", id
        try:
            tracker = Core.current_user().get_permitted_objects("EDIT", TimeTracker).get(id=id)
            self._update_actions[action](tracker)
        except TimeTracker.DoesNotExist:
            return rc.NOT_FOUND

    def _update_all(self, action):
        all = TimeTracker.objects.filter(active=True)
        for tracker in all:
            _update_actions[action](tracker)

    def delete(self, request, id):
        try:
            tracker = Core.current_user().get_permitted_objects("EDIT", TimeTracker).get(id=id)
            tracker.trash()
            return rc.DELETED
        except TimeTracker.DoesNotExist:
            return rc.NOT_FOUND












