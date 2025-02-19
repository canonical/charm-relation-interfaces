# Copyright 2024 pietro
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import scenario

from facade_charm.src.charm import FacadeCharm


def test_smoke():
    scenario.Context(FacadeCharm).run(
        "update-status",
        scenario.State()
    )
