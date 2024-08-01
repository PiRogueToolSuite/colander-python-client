from .base import BaseClientDomain
# NOTICE: Use official PEP 702 deprecations decorator if the project bump to python 3.13 or above
from deprecated import deprecated

class ObservableClientDomain(BaseClientDomain):

    def get_observable_types(self):
        return self._action(['observable_types', 'list'])

    def get_observable_type_by_short_name(self, short_name):
        dts = self.get_observable_types()
        for t in dts:
            if t['short_name'] == short_name:
                return t
        raise Exception(f"observable type does not exist: {short_name}")

    def get_observable(self, observable_id):
        return self._action(['observables', 'read'], {'id': observable_id})

    @deprecated(reason="Use get_observable(by_id) instead", version="1.0.4")
    def get_observable_by_id(self, observable_id):
        return self.get_observable(observable_id)

    def get_observables(self, case=None, name=None):

        # Inputs assertion
        # Here we can query without case_id if needed
        #if self._current_case is None and case is None:
        #    raise Exception("No current case set (use switch_case or provide it at function call)")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()

        # Query crafting
        search_params = dict()
        if case is not None:
            search_params['case_id'] = case['id']
        if name is not None:
            search_params['name'] = name

        return self._action(['observables', 'list'], search_params, validate=False)

    def create_observable(self, name=None, case=None, observable_type=None, extra_params=None):
        if name is None:
            raise Exception("No name provided")
        if self._get_current_case() is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if observable_type is None:
            raise Exception("No observable type provided")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        return self._action(
            ['observables', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'type': observable_type['id'],
                },
                **extra_params
            }
        )
