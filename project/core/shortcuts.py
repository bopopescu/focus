# -*- coding: utf-8 -*-
from core import Core
from core.forms import CommentForm
from core.models import User
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _

"""
Returns users in the same company as the current user
"""
def get_company_users():
    return User.objects.filter(company=Core.current_user())

def comment_block (request, object):
    """
    Returns the info needed to be used with the comments template

    Params:
        request: The request instance
        object: The object to comment on (for instance an Event)
    """
    
    if 'new_comment' in request.POST:
        comment_form = CommentForm(object, request.POST)

        if comment_form.is_valid():

            comment = comment_form.save(commit = False)
            comment.user = request.user
            comment.save()

            comment_form = CommentForm(object)

            request.message_success(_("Comment added successfully!"))

    else:
        comment_form = CommentForm(object)

    try:
        object.comments
    except:
        raise IntegrityError("Models using comments should have a generic relation named 'comments' to the Comment model!")
    return {'form': comment_form,
            'list': object.comments.all()}