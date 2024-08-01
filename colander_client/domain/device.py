from .base import BaseClientDomain
# NOTICE: Use official PEP 702 deprecations decorator if the project bump to python 3.13 or above
from deprecated import deprecated


class DeviceClientDomain(BaseClientDomain):
    def get_device_types(self):
        return self._action(['device_types', 'list'])

    def get_device_type_by_short_name(self, short_name):
        dts = self.get_device_types()
        for t in dts:
            if t['short_name'] == short_name:
                return t
        raise Exception(f"device type does not exist: {short_name}")

    def get_device(self, device_id):
        return self._action(['devices', 'read'], {'id': device_id})

    @deprecated(reason="Use get_device(by_id) instead", version="1.0.4")
    def get_device_by_id(self, device_id):
        return self.get_device(device_id)

    def get_devices(self, case=None, name=None):

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

        return self._action(['devices', 'list'], search_params, validate=False)

    def create_device(self, name=None, case=None, device_type=None, extra_params=None):
        if name is None:
            raise Exception("No name provided")
        if self._get_current_case() is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if device_type is None:
            raise Exception("No device type provided")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        return self._action(
            ['devices', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'type': device_type['id'],
                },
                **extra_params
            }
        )