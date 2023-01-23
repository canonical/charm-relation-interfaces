from scenario.structs import State
from interface_test import InterfaceTestCase


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
            assert data.get('prometheus_scrape_unit_name') == output_state.unit.name  # todo: fetch unit name


class IngressRequirerTest(InterfaceTestCase):
    EVENT = 'ingress-relation-changed'
    ROLE = 'requirer'

    def validate(self, output_state: State):
        pass