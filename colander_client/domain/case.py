from . import TlpPap
from .base import BaseClientDomain


class CaseClientDomain(BaseClientDomain):
    def get_case(self, case_id):
        return self._action(['cases', 'read'], {'id': case_id})

    def get_cases(self, name=None):
        # Query crafting
        search_params = dict()
        if name is not None:
            search_params['name'] = name

        return self._action(['cases', 'list'], search_params, validate=False)

    def create_case(self, name=None, description=None, tlp: TlpPap = None, pap: TlpPap = None, extra_params=None):
        if name is None:
            raise Exception("No name provided")
        if description is None:
            raise Exception("No description provided")
        if tlp is None:
            raise Exception("No tlp provided")
        if pap is None:
            raise Exception("No pap provided")

        # Sanitize inputs
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        return self._action(
            ['cases', 'create'],
            params={
                **{
                    'name': name,
                    'description': description,
                    'tlp': tlp,
                    'pap': pap,
                },
                **extra_params
            }
        )