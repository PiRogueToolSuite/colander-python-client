from .base import BaseClientDomain


class RelationClientDomain(BaseClientDomain):

    def get_relation(self, relation_id):
        return self._action(['relations', 'read'], {'id': relation_id})

    def get_relations(self, case=None, name=None):
        # Sanitize inputs
        if case is None:
            case = self._get_current_case()

        # Query crafting
        search_params = dict()
        if case is not None:
            search_params['case_id'] = case['id']
        if name is not None:
            search_params['name'] = name

        return self._action(['relations', 'list'], search_params, validate=False)

    def create_relation(self, name=None, case=None, obj_from=None, obj_to=None, extra_params=None):
        if name is None:
            raise Exception("No name provided")
        if self._get_current_case() is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if obj_from is None:
            raise Exception("No obj_from provided")
        if obj_to is None:
            raise Exception("No obj_to provided")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()
        if extra_params is None:
            extra_params = dict()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        print('from', obj_from['id'])
        print('to', obj_to['id'])

        return self._action(
            ['relations', 'create'],
            params={
                **{
                    'name': name,
                    'case': case['id'],
                    'obj_from': obj_from['id'],
                    'obj_to': obj_to['id'],
                },
                **extra_params
            }
        )
