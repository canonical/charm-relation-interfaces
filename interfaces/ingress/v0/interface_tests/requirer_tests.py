from scenario import State

from interface_test import interface_test_case


@interface_test_case(
    event='ingress-relation-created',
    role='requirer',
    input_state=State(leader=True),
)
def check_relation_data_foo(output_state: State):
    relation = output_state.relations[0]
    assert relation.local_app_data['foo'] == 'bar'
    assert not relation.local_unit_data
