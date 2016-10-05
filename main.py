#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import ProgrameApi

from models import User


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = User.query(User.email != None)
        for user in users:
            subject = 'This is a reminder!'
            body = 'Hello {}, try out Guess A Number!'.format(user.name)
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)


class UpdateAverageMovesRemaining(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        GuessANumberApi._cache_average_attempts()
        self.response.set_status(204)


class pushGameHistory(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        history_data = { 
            'user': self.request.get("user").decode('utf_8'),
            'score': self.request.get("score").decode('utf_8'),
            'action': self.request.get("action").decode('utf_8'), 
            'submission': self.request.get("submission").decode('utf_8'),
            'program_compiled' : self.request.get("program_compiled").decode('utf_8'),
            'result' : self.request.get("result").decode('utf_8')
            }
        ProgrameApi._push_game_history(history_data)
        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/cache_average_attempts', UpdateAverageMovesRemaining),
    ('/tasks/push_game_history', pushGameHistory)
], debug=True)
