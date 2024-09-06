from .base import BaseClientDomain


class PirogueExperiment(BaseClientDomain):

    def get_experiments(self, case=None, name=None):
        # Inputs assertion
        # Here we can query without case_id if needed

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()

        # Query crafting
        search_params = dict()
        if case is not None:
            search_params['case_id'] = case['id']
        if name is not None:
            search_params['name'] = name

        return self._action(['pirogue_experiments', 'list'], search_params, validate=False)

    def get_pirogue_experiment_analysis(self, experiment_id):
        return self._action(['pirogue_experiments', 'analysis'], {'id': experiment_id})

    def get_pirogue_experiment(self, experiment_id):
        return self._action(['pirogue_experiments', 'read'], {'id': experiment_id})

    def create_pirogue_experiment(self, name=None, case=None, pcap=None, socket_trace=None, sslkeylog=None, extra_params=None):

        # Inputs assertion
        if name is None:
            raise Exception("No name provided")
        if self._get_current_case is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if pcap is None:
            raise Exception("No pcap artifact provided")
        if socket_trace is None:
            raise Exception("No socket trace artifact provided")
        if sslkeylog is None:
            raise Exception("No ssl key log artifact provided")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        return self._action(
            ['pirogue_experiments', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'pcap': pcap['id'],
                    'socket_trace': socket_trace['id'],
                    'sslkeylog': sslkeylog['id'],
                },
                **extra_params
            }
        )
