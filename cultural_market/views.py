import otree
from otree.api import Currency as c, currency_range
from otree.session import SessionConfig
from otree.models.session import Session
from otree.export import _get_table_fields
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .models import Player

class Market(Page):
    form_model = models.Player

    def get_form_fields(self):
        fields = (
            ["rating_" + str(i) for i in range(Constants.num_artifacts)]
            + ["view_" + str(i) for i in range(Constants.num_artifacts)]
            + ["download_" + str(i) for i in range(Constants.num_artifacts)])
        return fields
    
    def get_context_data(self, **kwargs):
        context = super(Market, self).get_context_data(**kwargs)
        context["config"] = {
            "num_artifacts": Constants.num_artifacts,
            "num_worlds": Constants.num_worlds,
            "show_views": Constants.show_views,
            "show_downloads": Constants.show_downloads,
            "show_ratings": Constants.show_ratings
        }
        artifacts = [
            {
                "num": i,
                "rating_field": context["form"]["rating_{}".format(i)],
                "url": Constants.artifact_urls[i],
                "name": Constants.artifact_names[i],
                "filename": Constants.artifact_filenames[i],
                "num_ratings": 0,
                "mean_rating": 0,
                "num_views": 0,
                "num_downloads": 0
            }
            for i in range(Constants.num_artifacts)]
        context["num_artifacts"] = len(artifacts)
        context["artifacts"] = artifacts
        context["show_views"] = Constants.show_views
        context["show_downloads"] = Constants.show_downloads
        context["show_ratings"] = Constants.show_ratings
        
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
                for i in range(Constants.num_artifacts):
                    a = artifacts[i]
                    try:
                        a["mean_rating"] += player["rating_{}".format(i)]
                        a["num_ratings"] += 1
                    except TypeError:
                        pass
                    try:
                        a["num_views"] += player["view_{}".format(i)]
                    except TypeError:
                        pass
                    try:
                       a["num_downloads"] += player["download_{}".format(i)]
                    except TypeError:
                        pass
        for i in range(Constants.num_artifacts):
            a = artifacts[i]
            try:
                a["mean_rating"] = float(a["mean_rating"]) / float(a["num_ratings"])
            except ZeroDivisionError:
                a["mean_rating"] = 0
        return context

class Results(Page):
    pass


page_sequence = [
    Market
]
