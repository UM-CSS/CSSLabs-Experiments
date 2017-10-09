from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from configparser import ConfigParser

author = 'Edward L. Platt'

doc = """
Social influence in cultural markets. Bassed on Salganik, Dodds, and Watts 2006.
"""

config = ConfigParser()
config.read("cultural_market/market.cfg")

class Constants(BaseConstants):
    name_in_url = 'cultural_market'
    players_per_group = None
    num_rounds = 1
    num_artifacts = config.getint('experiment', 'num_artifacts')
    artifact_names, artifact_urls = zip(*[
        (s.split(";")[0].strip(), s.split(";")[1].strip())
        for s in config.get('experiment', 'artifacts').split('\n') if len(s.strip()) > 0])
    artifact_filenames = [s.split("/")[-1] for s in artifact_urls]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    for i in range(Constants.num_artifacts):
        locals()["rating_" + str(i)] = models.IntegerField(
            choices=[1,2,3,4,5],
            widget=widgets.RadioSelect())
    del i
