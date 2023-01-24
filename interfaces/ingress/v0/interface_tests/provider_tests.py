from scenario.structs import State, relation

from interface_test import InterfaceTestCase


class ProviderTestCase(InterfaceTestCase):
    ROLE = 'provider'

class IngressProviderTestCreated(ProviderTestCase):
    EVENT = 'ingress-relation-created'
    INPUT_STATE = State()

    # nothing happens on created

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data

    # # TODO: document this pattern to suppress schema validation i.e. if it's expected to be empty.
    # def validate_schema(data, schema):
    #     pass


class IngressProviderTestJoined(ProviderTestCase):
    EVENT = 'ingress-relation-joined'
    INPUT_STATE = State()

    # nothing happens on joined

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data


class IngressProviderTestChangedValid(ProviderTestCase):
    EVENT = 'ingress-relation-changed'
    INPUT_STATE = State(
        relations=[relation(
            # todo: endpoint is unknown/overwritten: find an elegant way to omit it here.
            #  perhaps input state is too general: we only need this relation meta:
            endpoint='ingress',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'host': '0.0.0.42',
                'model': 'bar',
                'name': 'baz',
                'port': '42',
            }
        )]
    )

    # on changed, if the remote side has sent valid data: our side is populated.

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_unit_data
        assert relation.local_app_data


class IngressProviderTestChangedInvalid(ProviderTestCase):
    EVENT = 'ingress-relation-changed'
    INPUT_STATE = State(relations=[relation(
        # todo: endpoint is unknown/overwritten: find an elegant way to omit it here.
        #  perhaps input state is too general: we only need this relation meta:
        endpoint='ingress',
        interface='ingress',
        remote_app_name='remote',
        remote_units_data={0: {
            'port': '42',
            'bubble': 'rubble'
        }}
    )]
    )

    # on changed, if the remote side has sent INvalid data: local side didn't publish anything either.

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data

    def validate_schema(relation, schema):
        pass

