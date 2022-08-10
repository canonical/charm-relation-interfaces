#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk
"""Template charm for generating tester charms."""
import json
import logging

import yaml
from jsonpath_ng.ext import parse
from ops.charm import CharmBase, RelationChangedEvent, RelationJoinedEvent, RelationCreatedEvent
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, Relation, BlockedStatus

from test_cases import get_test_cases

logger = logging.getLogger(__name__)

INITIAL_STEP = 0


class OperatorTemplateCharm(CharmBase):
    """Tester Charm."""

    RELATION_NAME = """{RELATION_NAME}"""
    TEST_CASES = """{TEST_CASES}"""

    _stored = StoredState()

    @property
    def step(self):
        return int(self._stored.step)

    @property
    def current(self):
        return self.states[self.step]

    @property
    def is_done(self) -> bool:
        return self.step >= len(self.states) - 1

    def __init__(self, *args):
        super().__init__(*args)
        self._load_test_cases()
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade)
        self._stored.set_default(step=INITIAL_STEP, started=False)
        relation_name = self.RELATION_NAME + "_relation"
        relation = self.on[relation_name]

        self.framework.observe(relation.created, self._on_relation_created)
        self.framework.observe(relation.joined, self._on_relation_joined)
        self.framework.observe(relation.changed, self._on_relation_changed)

        if self._stored.started is False:
            if self.framework.model.unit.is_leader():
                self.framework.model.app.status = ActiveStatus("Ready to start tests")
            self.framework.model.unit.status = ActiveStatus("Ready to start tests")
            self._stored.started = True

    def _load_test_cases(self):
        raw_tests = yaml.safe_load(self.TEST_CASES)
        self.states = get_test_cases(raw_tests).states

    def _on_upgrade(self, _):
        self._stored.step = INITIAL_STEP

    def _on_relation_joined(self, evt: RelationJoinedEvent):
        self._stored.step = INITIAL_STEP
        self._load_step(evt.relation, self.step)

    def _on_relation_created(self, evt: RelationCreatedEvent):
        self._stored.step = INITIAL_STEP
        self._load_step(evt.relation, self.step)

    def _on_relation_changed(self, evt: RelationChangedEvent):
        logger.warning("APP? %s == %s", evt.app.name, self.app.name)
        if evt.app.name == self.app.name:
            return
        if self.app.status == BlockedStatus(f"failed at step {str(self.step + 1)}"):
            return

        local_state = self.snapshot_state(evt)
        logger.warning(f"STATE:\n {json.dumps(local_state)}\n---")

        for path in self.current.remote:
            result = parse(path).find(json.dumps(local_state['remote']))
            logger.info("RESULTS:\n%s", json.dumps(result))
            if len(result) < 1:
                self.unit.status = self.app.status = BlockedStatus(f"failed at step {str(self.step + 1)}")
                return

        if not self.is_done:
            logger.info("Step %s of %s completed", str(self.step + 1), str(len(self.states)))
            self.unit.status = self.app.status = ActiveStatus(f"test {self.step + 1}/{len(self.states)} passed")
            self._next_step(evt.relation)
        else:
            logger.info("Step %s of %s completed - all done!", str(self.step + 1), str(len(self.states)))
            self.unit.status = self.app.status = ActiveStatus(f"test {self.step + 1}/{len(self.states)} passed (done)")

    def snapshot_state(self, evt):
        return {
            "local": {
                "application-data": {
                    key: val for key, val in evt.relation.data[self.model.app].items()
                },
                "related-units": {
                    self.model.unit.name: {
                        key: val for key, val in evt.relation.data[self.model.unit].items()
                    }
                },
            },
            "remote": {
                "application-data": {key: val for key, val in evt.relation.data[evt.app].items()},
                "related-units": {} if not evt.unit or not evt.unit in evt.relation.data else {
                    evt.unit.name: {
                        key: val for key, val in evt.relation.data[evt.unit].items()
                    },
                },
            },
        }

    def _next_step(self, relation: Relation):
        # increment stored step by one
        self._stored.step += 1
        self._load_step(relation, self._stored.step)

    def _load_step(self, relation: Relation, step_index: int):
        test = self.states[step_index]
        # populate unit and app data bags as specified by the test
        for obj, data in [
            (relation.data[self.unit], test.local.unit),
            (relation.data[self.app], test.local.app),
        ]:
            for k, v in data.items():
                obj[k] = str(v)

    def _on_config_changed(self, _):
        pass


if __name__ == "__main__":
    main(OperatorTemplateCharm)
