from operator import itemgetter
import random

import otree
from otree.api import Currency as c, currency_range
from otree.session import SessionConfig
from otree.models.session import Session
from otree.export import _get_table_fields
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .models import Player

class Main(Page):
    form_model = models.Player

    def get_form_fields(self):
        fields = (
            ["rating_" + str(i) for i in range(Constants.num_artifacts)]
            + ["view_" + str(i) for i in range(Constants.num_artifacts)]
            + ["download_" + str(i) for i in range(Constants.num_artifacts)])
        return fields
    
    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context["config"] = {
            "num_artifacts": Constants.num_artifacts,
            "num_worlds": Constants.num_worlds,
            "show_views": Constants.show_views,
            "show_downloads": Constants.show_downloads,
            "show_ratings": Constants.show_ratings
        }
        artifacts = [
            {
                "rating_field": context["form"]["rating_{}".format(i)],
                "true_rating_count": 0,
                "total_rating": 0,
                "random": random.random()
            }
            for i in range(Constants.num_artifacts)]
        for i, a in enumerate(Constants.artifacts):
            artifacts[i]["num"] = i
            artifacts[i].update(a)
        context["num_artifacts"] = len(artifacts)
        context["show_views"] = Constants.show_views
        context["show_downloads"] = Constants.show_downloads
        context["show_ratings"] = Constants.show_ratings
        context["title"] = Constants.title
        
        player_fields = _get_table_fields(Player)
        Subsession = models_module = otree.common_internal.get_models_module('cultural_market').Subsession
        rows = []
        for session in Session.objects.order_by('id'):
            subsession = Subsession.objects.filter(session_id=session.id, round_number=1).values()
            if not subsession:
                continue
            subsession = subsession[0]
            subsession_id = subsession['id']
            for player in Player.objects.filter(subsession_id=subsession_id).order_by('id').values():
                if player["world"] != context["player"].world:
                    continue
                for i in range(Constants.num_artifacts):
                    a = artifacts[i]
                    try:
                        a["total_rating"] += player["rating_{}".format(i)]
                        a["true_rating_count"] += 1
                    except TypeError:
                        pass
                    try:
                        a["view_count"] += player["view_{}".format(i)]
                    except TypeError:
                        pass
                    try:
                       a["download_count"] += player["download_{}".format(i)]
                    except TypeError:
                        pass
        for i in range(Constants.num_artifacts):
            a = artifacts[i]
            try:
                m = float(a["total_rating"]) / float(a["true_rating_count"])
                a["mean_rating"] = (
                    (m*float(a["true_rating_count"]) + a["start_rating"]*a["rating_count"])
                    / (float(a["true_rating_count"]) + float(a["rating_count"])))
            except ZeroDivisionError:
                a["mean_rating"] = a["start_rating"]
        if context["player"].world == 0:
            artifacts = sorted(artifacts, key=itemgetter("random"), reverse=True)
        else:
            artifacts = sorted(artifacts, key=itemgetter(Constants.sort_by), reverse=True)
        context["artifacts"] = artifacts
        return context

class Results(Page):
    pass


page_sequence = [
    Main
]
