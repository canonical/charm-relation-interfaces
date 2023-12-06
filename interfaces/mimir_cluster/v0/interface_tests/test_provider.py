import scenario
import yaml
from interface_tester import Tester


def test_unhappy():
    # GIVEN an initial empty state (worker did not submit roles yet)
    t = Tester(state_in=scenario.State())

    # WHEN we get a relation-changed event (or any other, for that matter)
    t.run("mimir_cluster_relation_changed")

    # THEN we don't publish anything either
    t.assert_relation_data_empty()


def test_happy():
    # GIVEN an initial state where the worker did submit roles
    t = Tester(
        state_in=scenario.State(
            relations=[scenario.Relation(
                "foo",
                interface="mimir_cluster",
                # supposing this is the correct format:
                remote_app_data={"roles": yaml.safe_dump(
                    ["write", "read", "querier", "collector"]
                )
                }
            )
            ]
        )
    )

    # WHEN we get a relation-changed event
    t.run("mimir_cluster_relation_changed")

    # THEN we have done our part
    t.assert_schema_valid()
