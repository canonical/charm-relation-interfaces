from typing import Optional
from unittest.mock import patch

import pytest
from ops.charm import CharmBase
from ops.framework import Framework

# could be in a separate file, we don't really care.
# IRL, this will be in /src/charm.py
class ZincOperatorCharm(CharmBase):
    def __init__(self, framework: Framework, key: Optional[str] = None):
        super().__init__(framework, key)
        if not self.config["required_config"""] == "without which your charm will bork":
            raise RuntimeError()


# IRL, this will be in /tests/interfaces/test_relation_interfaces.py

# this will work regardless. However, unless you have installed our
# pytest plugin, you won't be able to run the test yourself. For that reason, we'd rather omit the
# test_ prefix to avoid pytest collecting them automatically.
@pytest.mark.interface_test(
    interface_name='prometheus-scrape',
    config={"required_config": "without which your charm will bork"},
)
def prom_scrape_compatibility():
    # setup whatever mocking you need to,
    # to make the charm run in isolation
    patch('lightkube.do_this_and_that', lambda: None)
    patch('charm.ZincOperatorCharm.do_this_and_that', lambda: None)
    ZincOperatorCharm._call_google_dot_com = lambda self: 404
    yield ZincOperatorCharm

    # your chance to undo any damage
