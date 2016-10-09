#!/usr/bin/env python
""" Handlers for cron jobs and tasks

    Contains functions for various cron jobs and tasks associated
    with programe-api.
"""


# imports

import webapp2
from google.appengine.api import mail, app_identity
from api import ProgrameApi
from User import User
from GameHistory import GameHistory


# crons

class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send an email to any users who have a failed game each day"""

        app_id = app_identity.get_application_id()
        users = User.query(User.email != None)
        for user in users:
            # if user has failed a their last level

            history = GameHistory.query(
                GameHistory.user == user.key).order(-GameHistory.date).get()
            if not history.program_compiled:
                subject = 'Dont give up!'
                body = 'Hello {}, you recently failed a challenge on < ProgGrAME />, now is the time\
                        to go back and complete it!!!'.format(user.name)
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


# tasks

class pushGameHistory(webapp2.RequestHandler):
    def post(self):
        """Push the current move or action into our game history,
        since we dont rely on history we can push it into the task queue."""

        ProgrameApi._push_game_history({
            'user': self.request.get("user"),
            'score': self.request.get("score"),
            'action': self.request.get("action"),
            'submission': self.request.get("submission"),
            'program_compiled': self.request.get("program_compiled"),
            'level': self.request.get("level")
            })
        self.response.set_status(204)


# register routes for crons and tasks

app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/push_game_history', pushGameHistory)
], debug=True)
