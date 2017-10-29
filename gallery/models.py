from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from configparser import ConfigParser
import random

author = 'Edward L. Platt'

doc = """
Social influence in cultural markets. Bassed on Salganik, Dodds, and Watts 2006.
"""

config = ConfigParser()
config.read("cultural_market/market.cfg")


class Constants(object):
    name_in_url = 'cultural_market'
    players_per_group = None
    num_rounds = 1
    
    show_views = config.getboolean('experiment', 'show_views')
    show_downloads = config.getboolean('experiment', 'show_downloads')
    show_ratings = config.getboolean('experiment', 'show_ratings')
    num_worlds = config.getint('experiment', 'num_worlds')
    
    artifact_rows = []
    for s in config.get('experiment', 'artifacts').split('\n'):
        if len(s.strip()) > 0:
            artifact_rows.append(s)
    artifact_names = []
    artifact_init = []
    artifact_urls = []
    for row in artifact_rows:
       artifact_name, artifact_i, artifact_u = row.split(";")
       artifact_names.append(artifact_name)
       artifact_init.append(artifact_i)
       artifact_urls.append(artifact_u)
    num_artifacts = len(artifact_names)
    artifact_filenames = []
    for s in artifact_urls:
        artifact_filenames.append(s.split("/")[-1])
    artifact_const = []
    for i in range(num_artifacts):
        artifact_const.append({
            "num": i,
            "url": artifact_urls[i],
            "name": artifact_names[i],
            "filename": artifact_filenames[i],
            "init_num_views": int(artifact_init[i].split(",")[0].strip()),
            "init_num_downloads": int(artifact_init[i].split(",")[1].strip()),
            "init_num_ratings": int(artifact_init[i].split(",")[2].strip()),
            "init_mean_rating": float(artifact_init[i].split(",")[3].strip())
        })


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
    