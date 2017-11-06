from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from configparser import ConfigParser
import random
import yaml

author = 'Edward L. Platt'

doc = """
Social influence in cultural markets. Bassed on Salganik, Dodds, and Watts 2006.
"""

with open("cultural_market/config.yaml", "r") as f:
    config = yaml.load(f)

class Constants(object):
    name_in_url = 'gallery'
    players_per_group = None
    num_rounds = 1
    
    show_views = bool(config.get("show_views", False))
    show_downloads = bool(config.get("show_downloads", False))
    show_ratings = bool(config.get("show_ratings", False))
    sort_by = config.get("sort_by", "random")
    num_worlds = int(config.get("num_worlds", 8))
    num_columns = int(config.get("num_columns", 1))
    title = config.get("title", "Gallery")
    
    artifacts = config["artifacts"]
    for a in artifacts:
        a["view_count"] = int(a.get("view_count", 0))
        a["download_count"] = int(a.get("download_count", 0))
        a["rating_count"] = int(a.get("rating_count", 0))
        a["start_rating"] = float(a.get("start_rating", 2.5))
    num_artifacts = len(artifacts)

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.world = random.randint(0, Constants.num_worlds)

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
        locals()["download_" + str(i)] = models.IntegerField(blank=True)
    world = models.IntegerField(initial=0)
    del i
    
    comments = models.TextField(verbose_name='Comments:')
    