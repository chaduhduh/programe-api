#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import ProgrameApi
from datetime import datetime, timedelta

from models import User, GameHistory


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        print "seiding email"
        users = User.query(User.email != None)
        for user in users:
            history = GameHistory.query(GameHistory.user == user.key, GameHistory.program_compiled == False)    # if user has failed a level encourage them
            if history:
                subject = 'This is a reminder!'
                body = 'Hello {}, try out Guess A Number!'.format(user.name)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


class pushGameHistory(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        history_data = { 
            'user': self.request.get("user"),
            'score': self.request.get("score"),
            'action': self.request.get("action"), 
            'submission': self.request.get("submission"),
            'program_compiled' : self.request.get("program_compiled"),
            'level' : self.request.get("level")
            }
        ProgrameApi._push_game_history(history_data)
        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/push_game_history', pushGameHistory)
], debug=True)
