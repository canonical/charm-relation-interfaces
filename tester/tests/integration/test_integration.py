#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
"""Integration tests for the tester charm."""

import logging

import pytest
from pytest_operator.plugin import OpsTest

from main import in_tempdir, _build_tester_charm

TRAEFIK_NAME = "traefik-k8s"

logger = logging.getLogger(__name__)


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    """Deploys a tester charm, a charm to test, relates them and waits."""

    await in_tempdir(ops_test, "ingress", "requires", _build_tester_charm)

    # await ops_test.model.set_config({"update-status-hook-interval": "10s"})
    # await ops_test.model.deploy(
    #     TRAEFIK_NAME,
    #     application_name=TRAEFIK_NAME,
    #     channel="edge",
    #     config={"routing_mode": "path", "external_hostname": "foo.bar"},
    # )
    # await ops_test.model.wait_for_idle(apps=[TRAEFIK_NAME])
    # await is_compatible(
    #     ops_test, name_of_charm_to_test=TRAEFIK_NAME, interface="ingress", tester_role="requires"
    # )
