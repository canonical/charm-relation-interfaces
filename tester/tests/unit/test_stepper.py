import unittest

from ops.testing import Harness

from charm import OperatorTemplateCharm
from main import generate_meta
from test_cases import TestCase, DataBagContents

MINIMAL_TEST_CASE = """
states:
  - local: # Tester Charm
      app:
        version: 1
      unit: {}
    remote:
      - $.application-data.version
      - $.related-units.*.model
      - $.related-units.*.unit
  - local: 
      app:
        version: 1
      unit: 
        foo: bar
    remote:
      - $.related-units.*.bar
      - $.related-units.*.unit
"""


class PatchedCharm(OperatorTemplateCharm):
    TEST_CASES = MINIMAL_TEST_CASE
    RELATION_NAME = "ingress"


class TestCharm(unittest.TestCase):
    def setUp(self) -> None:
        meta = generate_meta("ingress", "provides")
        self.harness = Harness(PatchedCharm, meta=meta)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_something(self):
        current = self.harness.charm._stored.step
        assert current == 0
        expected = TestCase(
            local=DataBagContents(
                unit={},
                app={'version': 1}
            ),
            remote=[
                "$.application-data.version",
                "$.related-units.*.model",
                "$.related-units.*.unit",
            ],
        )

        assert self.harness.charm.states[current] == expected
