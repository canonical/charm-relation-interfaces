import abc
from typing import Literal

from scenario.structs import State

__TESTS__ = [
    "IngressProviderTest",
]


# declare the name of the interface you're testing (it might be different from the directory name)
#  this is a REQUIRED global variable. Without it, this test case won't be valid.
INTERFACE_NAME: str = 'ingress'

class InterfaceTestCase(abc.ABC):
    INPUT_STATE: State = None

    @property
    @abc.abstractmethod
    def ROLE(self) -> Literal['provider', 'requirer']:
        raise NotImplementedError()
    @property
    @abc.abstractmethod
    def EVENT(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self, output_state: State):
        raise NotImplementedError("validate")


class IngressProviderTest(InterfaceTestCase):
    EVENT = 'ingress-relation-created'
    INPUT_STATE = State()
    ROLE = 'provider'

    def validate(self, output_state: State):
        scrape_relation_out = output_state.relations[0]
        if output_state.leader:
            assert scrape_relation_out.local_app_data.get('alert_rules')  # todo: json schema validation?
            assert scrape_relation_out.local_app_data.get('scrape_jobs')  # todo: json schema validation?
            assert scrape_relation_out.local_app_data.get('scrape_metadata')  # todo: json schema validation?
        else:
            assert scrape_relation_out.local_app_data == {}

        for unit, data in scrape_relation_out.local_unit_data:
            assert data.get('prometheus_scrape_unit_address')
            assert data.get('prometheus_scrape_unit_name') == charm.unit.name  # todo: fetch unit name

