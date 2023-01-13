# in order to write these tests, you should install "scenario", the scenario-based testing lib for ops.
# That will provide you completion and documentation for using the State object.
# at the time of writing, that can only be installed from sources (build a wheel from https://github.com/PietroPasotti/ops-scenario/tree/stripped)
# todo: as soon as https://github.com/canonical/operator/pull/887 merges, update this.
import abc
from typing import Literal

from scenario.structs import State, network, NetworkSpec


# declare in a variable called "__TESTS__" the exhaustive list of classes,
#  matching the InterfaceTestCase protocol, that are meant to test your interface.

__TESTS__ = [
    "MyInterfaceProviderCreatedTest",
]

# declare the name of the interface you're testing (it might be different from the directory name)
#  this is a REQUIRED global variable. Without it, this test case won't be valid.
INTERFACE_NAME: str = 'interface-name'


# this is the protocol that a test case must match: feel free
#  to keep it on top of your test file as reference.
class InterfaceTestCase(abc.ABC):
    INPUT_STATE: State = None

    @abc.abstractmethod
    @property
    def ROLE(self) -> Literal['provider', 'requirer']:
        raise NotImplementedError()
    @abc.abstractmethod
    @property
    def EVENT(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self, output_state: State):
        raise NotImplementedError("validate")


class MyInterfaceProviderCreatedTest(InterfaceTestCase):
    # declare which role of the interface this test is meant to verify.
    ROLE = 'provider'

    # declare which event this test is about.
    EVENT = 'interface-name-relation-created',

    # you can override INPUT_STATE to provide a 'template' for the test case to build upon.
    #  99% of the time you won't need this: the test runner will inject for you a relation object
    #  matching the spec found in the charm-under-test's metadata.yaml.

    # However, suppose, if this relation interface requires a specific network binding
    #  in order to function, you could:
    INPUT_STATE = State(
        networks=[
            NetworkSpec(
                name='my-network',
                bind_id=0,
                network=network(egress_subnets=("1.1.1.42/42",))
            )
        ]
    )

    # this function should contain the assertion that the test case represents.
    def validate(self, output_state: State):
        # here: write assertion code that checks that, if the charm implementing the provider side were
        #  to receive an interface-name-relation-created event with that state, the charm would *do the right thing*,
        #  whatever that means in the context of this interface.
        #  for example, if the charm is meant to set application data as a response to this event, you could do:
        assert output_state.relations[0].local_app_data['baz'] == 'qux'


# also fill in:
class MyInterfaceRequirerChangedTest(InterfaceTestCase):
    ROLE = 'requirer'
    EVENT = 'interface-name-relation-changed',

    def validate(self, output_state: State):
        pass

