"""Rank Model Definitions"""

from protorpc import messages


class Rank(messages.Message):
    """Defines a rank"""

    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    attempts_used = messages.IntegerField(3, required=True)
    score = messages.IntegerField(4, required=True)
    rank = messages.IntegerField(5, required=True)


class RankForm(messages.Message):
    """List of Rank objects for output"""
    ranks = messages.MessageField(Rank, 1, repeated=True)
