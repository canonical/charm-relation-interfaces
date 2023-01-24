from scenario.structs import State

from interface_test import InterfaceTestCase


class RequirerTestCase(InterfaceTestCase):
    ROLE = 'requirer'


class IngressRequirerTestCreated(RequirerTestCase):
    EVENT = 'ingress-relation-created'
    INPUT_STATE = State(leader=True)

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert relation.local_app_data
        assert not relation.local_unit_data
