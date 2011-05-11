# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.announcements.models import Announcement

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ("title", "text", "attachment",)
        #exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company')