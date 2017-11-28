import math
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

def parse_world_counts(num_worlds, o):
    if isinstance(o, list):
        assert(len(o) == num_worlds)
        return [int(count) for count in o]
    return [int(o) for i in range(num_worlds)]

def parse_world_ratings(num_worlds, o):
    if isinstance(o, list):
        assert(len(o) == num_worlds)
        return [float(count) for count in o]
    return [float(o) for i in range(num_worlds)]

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
        a["world_view_count"] = parse_world_counts(num_worlds, a.get("view_count", 0))
        a["world_download_count"] = parse_world_counts(num_worlds, a.get("download_count", 0))
        a["world_rating_count"] = parse_world_counts(num_worlds, a.get("rating_count", 0))
        a["world_start_rating"] = parse_world_ratings(num_worlds, a.get("rating", 3))
    num_artifacts = len(artifacts)
    num_rows = int(math.ceil(float(num_artifacts) / num_columns))

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.world = random.randint(0, Constants.num_worlds - 1)
            p.cols = Constants.num_columns
            p.rows = Constants.num_rows
            p.direction = "down,right"

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
        locals()["download_" + str(i)] = models.IntegerField(blank=True)
        locals()["time_ms_" + str(i)] = models.IntegerField(blank=True)
        locals()["position_" + str(i)] = models.IntegerField()
    del i
    world = models.IntegerField(initial=0)
    rows = models.IntegerField()
    cols = models.IntegerField()
    direction = models.TextField()
    user_agent = models.TextField()
        