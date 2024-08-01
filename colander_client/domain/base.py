
class BaseClientDomain:
    def _action(self, keys, params=None, validate=True, overrides=None,
                action=None, encoding=None, transform=None):
        raise NotImplementedError("Not overridden by Client")

    def _get_current_case(self):
        raise NotImplementedError("Not overridden by Client")

    def _get_global_progress_callback(self):
        raise NotImplementedError("Not overridden by Client")

    @staticmethod
    def _unpack_ids_if_any(params):
        # WARNING: This assumes we will never have 'extra_params' items containing

        # Deep copy is unnecessary there since
        # potential modifications are only done at dict root level
        params = params.copy()
        for k, v in params.items():
            if isinstance(v, dict):
                if 'id' in v:
                    params[k] = v['id']
            # May contain list of dict to unpack
            if isinstance(v, list):
                params[k] = [ e['id'] if isinstance(e, dict) and 'id' in e else e for e in v ]

        return params

    @staticmethod
    def _no_progress(*args):
        pass
