import os

from coreapi import Client as CoreApiClient
from coreapi.auth import TokenAuthentication

from .domain.artifact import ArtifactClientDomain
from .domain.case import CaseClientDomain
from .domain.device import DeviceClientDomain
from .domain.observable import ObservableClientDomain
from .domain.pirogue_experiment import PirogueExperiment
from .domain.relation import RelationClientDomain
from .domain.team import TeamClientDomain


class Client(ArtifactClientDomain,
             CaseClientDomain,
             DeviceClientDomain,
             ObservableClientDomain,
             PirogueExperiment,
             RelationClientDomain,
             TeamClientDomain):
    _client: CoreApiClient

    _base_url = None
    _api_url = None

    _current_case = None
    _global_progress_callback = None

    def __init__(self, base_url=None, api_key=None):

        if base_url is None:
            base_url = os.getenv("COLANDER_PYTHON_CLIENT_BASE_URL")

        if api_key is None:
            api_key = os.getenv("COLANDER_PYTHON_CLIENT_API_KEY")

        if base_url is None:
            raise Exception("No API base url provided (COLANDER_PYTHON_CLIENT_BASE_URL)")

        if api_key is None:
            raise Exception("No API Key provided (COLANDER_PYTHON_CLIENT_API_KEY)")

        self._base_url = base_url
        self._api_url = f"{self._base_url}/api"

        auth = TokenAuthentication(
            scheme='Token',
            token=api_key
        )

        self._client = CoreApiClient(auth=auth)
        self._root_document = self._client.get(f'{self._api_url}/schema', format='corejson')

    def _action(self, keys, params=None, validate=True, overrides=None,
                action=None, encoding=None, transform=None):
        return self._client.action(self._root_document, keys,
                                   params=params, validate=validate,
                                   overrides=overrides, action=action,
                                   encoding=encoding, transform=transform)

    def switch_case(self, case):
        self._current_case = case

    def _get_current_case(self):
        return self._current_case

    def set_global_progress_callback(self, progress_callback):
        self._global_progress_callback = progress_callback

    def _get_global_progress_callback(self):
        return self._global_progress_callback

