from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Edward L. Platt'

doc = """
Collect feedback and display "thank you" page.
"""


class Constants(BaseConstants):
    name_in_url = 'feedback'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comments = models.TextField(verbose_name='Comments:', blank=True)

