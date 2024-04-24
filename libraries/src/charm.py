#!/usr/bin/env python3
# Copyright 2024 simme
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following tutorial that will help you
develop a new k8s charm using the Operator Framework:

https://juju.is/docs/sdk/create-a-minimal-kubernetes-charm
"""

import logging

import ops

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class LibrariesCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        raise Exception("This charm is not meant to be deployed as it's a library for charm interfaces.")


if __name__ == "__main__":  # pragma: nocover
    ops.main(LibrariesCharm)  # type: ignore
