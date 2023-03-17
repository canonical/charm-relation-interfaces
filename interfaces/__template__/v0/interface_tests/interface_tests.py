# in order to write these tests, you should install "scenario", the scenario-based testing lib for ops.
# That will provide you completion and documentation for using the State object.
from scenario import State, Network

# this is an ABC: it will guide you through implementing all required attributes and methods.
from tester.plugin.interface_test import interface_test_case


@interface_test_case(
    # declare which role of the interface this test is meant to verify.
    role='provider',

    # declare which event this test is about.
    event='interface-name-relation-created',

    # you can override INPUT_STATE to provide a 'template' for the test case to build upon.
    #  99% of the time you won't need this: the test runner will inject for you a relation object
    #  matching the spec found in the charm-under-test's metadata.yaml.

    # However, suppose, if this relation interface requires a specific network binding
    #  in order to function, you could:
    input_state=State(
        networks=[
            Network(
                name='my-network',
                bind_addresses=[],
                ingress_addresses=[],
                egress_subnets=["1.1.1.42/42"]
            )
        ]
    )
)
def assert_my_interface_provider_required(output_state: State):
    # here: write assertion code that checks that, if the charm implementing the provider side were
    #  to receive an interface-name-relation-created event with that state, the charm would *do the right thing*,
    #  whatever that means in the context of this interface.
    #  for example, if the charm is meant to set application data as a response to this event, you could do:
    assert output_state.relations[0].local_app_data['baz'] == 'qux'
    assert output_state.status.unit == 'active', 'idle'


@interface_test_case(
    role='requirer',
    event='interface-name-relation-changed')
def assert_my_interface_provider_required(output_state: State):
    pass
