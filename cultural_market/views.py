from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Market(Page):
    form_model = models.Player

    def get_form_fields(self):
        return ["rating_" + str(i) for i in range(Constants.num_artifacts)]
    
    def get_context_data(self, **kwargs):
        context = super(Market, self).get_context_data(**kwargs)
        context["num_artifacts"] = Constants.num_artifacts
        context["artifacts"] = [
            {
                "num": i,
                "rating_field": context["form"]["rating_{}".format(i)],
                "url": Constants.artifact_urls[i],
                "name": Constants.artifact_names[i],
                "filename": Constants.artifact_filenames[i]
            }
            for i in range(Constants.num_artifacts)]
        return context


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Market,
    ResultsWaitPage,
    Results
]
