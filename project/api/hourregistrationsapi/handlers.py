from piston.handler import BaseHandler
from piston.utils import rc
from api.hourregistrationsapi.forms import TimeTrackerForm
from api.hourregistrationsapi.models import TimeTracker
from app.hourregistrations.models import HourRegistration
from app.orders.models import Order
from core import Core
from django.utils.translation import ugettext as _

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
    fields = ('id', 'name', 'active', 'time_info', 'is_running', ('time_periods', ('start', 'end', 'done',),),)


    @classmethod
    def time_info(cls, time_tracker):
        return time_tracker.time_info()

    @classmethod
    def is_running(cls, time_tracker):
        return time_tracker.is_running()


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

        
    def update(self, request, id=None):

        if id:
            trackers = [Core.current_user().get_permitted_objects("EDIT", TimeTracker).get(id=id)]
        else:
            trackers = Core.current_user().get_permitted_objects("EDIT", TimeTracker).all()
        for tracker in trackers:
            try:
                self._do_update(request, tracker)
            except ValueError as e:
                return {'error': str(e)}

        return {'success': True}

    def _do_update(self, request, tracker):
        action = request.PUT.get('action', False)
        {
        'stop': lambda: self._handle_stop(request, tracker),
        'start': lambda: tracker.start_new(),
        'pause': lambda: tracker.pause()
        }[action]()



    def _handle_stop(self, request, tracker):
        description = request.PUT.get('description', False)
        order = int(request.PUT.get('order', False))
        if description and order:
            order = Order.objects.get(id=order)
            tracker.stop_and_save(description, order)
        else:
            raise ValueError(_("Order or description missing"))
        

    def delete(self, request, id):
        try:
            tracker = Core.current_user().get_permitted_objects("EDIT", TimeTracker).get(id=id)
            tracker.trash()
            return rc.DELETED
        except TimeTracker.DoesNotExist:
            return rc.NOT_FOUND












