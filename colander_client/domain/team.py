from .base import BaseClientDomain


class TeamClientDomain(BaseClientDomain):
    def get_team(self, team_id):
        return self._action(['teams', 'read'], {'id': team_id})
    def get_teams(self, name=None):
        # Query crafting
        search_params = dict()
        if name is not None:
            search_params['name'] = name

        return self._action(['teams', 'list'], search_params, validate=False)
