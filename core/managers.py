from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta   
from django.db import models  
from django.conf import settings
from django.http import Http404
from core.middleware import *

class PersistentManager(models.Manager):
    
    def for_company(self, *args, **kwargs):
        
        if 'deleted' in kwargs:
            deleted = kwargs['deleted']
        else:
            deleted = False
        
        try:
            u = get_current_user()
            
            if u.is_anonymous():
                HttpResponseRedirect("/accounts/")
      
            company = get_current_user().get_profile().company
                     
            if deleted == None:
                qs = self.get_query_set().filter(company = company)
            else:
                qs = self.get_query_set().filter(deleted = deleted, company = company) 

            return qs 
            
        except:    
            raise Http404
        
    def for_user(self, *args, **kwargs):
        u = get_current_user()
        
        if u.is_anonymous():
            HttpResponseRedirect("/accounts/")
        
        permitted = []       
               
        try:
            qs = self.for_company(*args, **kwargs)
            for l in qs.all():
                if get_current_user().has_perm('view', l):
                    permitted.append(l.id)
        except:   
            raise Http404
        
        qs = self.get_query_set().filter(id__in=permitted)
        
        return qs