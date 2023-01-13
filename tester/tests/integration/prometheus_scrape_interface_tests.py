from scenario.scenario import Scenario
from scenario.structs import *


def get_endpoint_from_meta(meta, interface):
    raise NotImplementedError()


def check_compliance(
        charm,
        config: Dict[str, str],
        leader: Optional[bool],
        event_name: str,
        interface: str,
        remote_app_data=None,
        # todo: here should by default be the juju-injected fields
        remote_units_data=None,
        remote_app_name: str = 'remote'):
    """Validate that the provided charm satisfies the prometheus-scrape relation spec."""
    relation_spec = relation(
        endpoint=get_endpoint_from_meta(charm.meta, interface),
        interface=interface,
        remote_app_name=remote_app_name,  # owner of the remote end's databags
        remote_unit_ids=list(int(x) for x in remote_units_data),
        remote_app_data=remote_app_data or {},
        remote_units_data=remote_units_data or {"0": {}}
    )

    scene = Scene(
        event(event_name),
        context=Context(
            state=State(
                relations=[
                    relation_spec,
                ],
                config=config,
                leader=leader  # if None: parametrize on True AND False
            )
        )
    )

    scenario = Scenario(
        CharmSpec(
            charm,
            meta=charm.meta,  # todo: cast from CharmMeta to CharmSpec.meta (Dict)
        )
    )

    out = scenario.play(scene)

    return out.context_out.state


class RelationInterfaceTester:
    def __init__(self, tester_spec: "TesterSpec"):
        self.spec = tester_spec
        self.env = None

    def run(self):
        for case_definition, method in self._gather_cases():
            output_state = check_compliance(
                **case_definition)
            method(output_state)


class MyTester(RelationInterfaceTester):
    @case(event='prometheus-scrape-relation-created',
          remote_app_data={})
    def check_relation_changed(self, output_state: State):
        pass
        # todo assert behaviour on empty remote data

    @case(event='prometheus-scrape-relation-changed',
          remote_app_data={'foo': 'bar'})
    def check_relation_changed(self, output_state: State):
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

    @case(event='custom-hook')
    def on_custom_event(self, output_state):
        pass
