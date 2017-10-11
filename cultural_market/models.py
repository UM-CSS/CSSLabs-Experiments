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
    artifact_names, artifact_urls = zip(*[
        (s.split(";")[0].strip(), s.split(";")[1].strip())
        for s in config.get('experiment', 'artifacts').split('\n') if len(s.strip()) > 0])
    artifact_filenames = [s.split("/")[-1] for s in artifact_urls]
    num_artifacts = len(artifact_names)
    show_views = config.getboolean('experiment', 'show_views')
    show_downloads = config.getboolean('experiment', 'show_downloads')
    show_ratings = config.getboolean('experiment', 'show_ratings')
    num_worlds = config.getint('experiment', 'num_worlds')

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    for i in range(Constants.num_artifacts):
        locals()["rating_" + str(i)] = models.IntegerField(
            choices=[1,2,3,4,5],
            widget=widgets.RadioSelect(),
            blank=True)
    for i in range(Constants.num_artifacts):
        locals()["view_" + str(i)] = models.IntegerField(blank=True)
    for i in range(Constants.num_artifacts):
        locals()["download_" + str(i)] = models.BooleanField(blank=True)
    world = models.IntegerField(initial=0)
    del i
