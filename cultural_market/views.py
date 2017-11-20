from operator import itemgetter
import math
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
            + ["download_" + str(i) for i in range(Constants.num_artifacts)]
            + ["time_ms_" + str(i) for i in range(Constants.num_artifacts)]
            + ["position_" + str(i) for i in range(Constants.num_artifacts)]
            + ["user_agent"])
        
        return fields
    
    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context["config"] = {
            "num_artifacts": Constants.num_artifacts,
            "num_worlds": Constants.num_worlds,
            "show_views": Constants.show_views,
            "show_downloads": Constants.show_downloads,
            "show_ratings": Constants.show_ratings,
            "title": Constants.title
        }
        
        # Generate artifact list and related variables
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
            artifacts[i]['view_count'] = a["world_view_count"][self.player.world]
            artifacts[i]['download_count'] = a["world_download_count"][self.player.world]
            artifacts[i]['rating_count'] = a["world_rating_count"][self.player.world]
            artifacts[i]['start_rating'] = a["world_start_rating"][self.player.world]
        context["num_artifacts"] = len(artifacts)
        
        # Included varaibles generated for this player's subsession
        context["world"] = self.player.world
        
        # Calculate views, downloads, and rating
        # This would make a lot more sense in a model class, sorry! -Ed
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
                    # Sum and count all real ratings
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
                # Figure out mean for real ratings
                m = float(a["total_rating"]) / float(a["true_rating_count"])
                a["mean_rating"] = (
                    (m*float(a["true_rating_count"]) + a["start_rating"]*a["rating_count"])
                    / (float(a["true_rating_count"]) + float(a["rating_count"])))
            except ZeroDivisionError:
                a["mean_rating"] = a["start_rating"]
        if context["player"].world == 0:
            artifacts = sorted(artifacts, key=itemgetter("random"), reverse=True)
        else:
            # Start with a random sort so that ties are broken randomly
            artifacts = sorted(artifacts, key=itemgetter("random"), reverse=True)
            artifacts = sorted(artifacts, key=itemgetter(Constants.sort_by), reverse=True)
        for rank, a in enumerate(artifacts):
            a["rank"] = rank + 1

        # Insert values related to artifact layout
        context["column_ids"] = range(Constants.num_columns)
        # Sort artifacts into 2-D list ([row][col]) based on number of columns
        # It's easiest to construct in [col][row] order and then transpose
        artifacts = list(reversed(artifacts))
        artifacts_by_col = []
        while len(artifacts) > 0:
            row = []
            for i in range(Constants.num_rows):
                try:
                    row.append(artifacts.pop())
                except IndexError:
                    break
            artifacts_by_col.append(row)
        artifacts_by_row = list(zip(*artifacts_by_col))
        context["artifacts_by_row"] = artifacts_by_row
        
        return context

class Survey(Page):
    form_model = models.Player
    form_fields = ['comments']

class ThankYou(Page):
    pass

class Instructions(Page):
    pass

page_sequence = [
    Instructions,
    Main,
    Survey,
    ThankYou
]
