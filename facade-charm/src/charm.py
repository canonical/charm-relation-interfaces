#!/usr/bin/env python3
# Copyright 2024 pietro
# See LICENSE file for licensing details.
import json
import logging
from itertools import chain
from pathlib import Path
from typing import Dict, Optional

import ops
import yaml
from ops import ActiveStatus

logger = logging.getLogger(__name__)


class FacadeCharm(ops.CharmBase):
    """Charming facade."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.collect_unit_status, self._on_collect_unit_status)
        self.framework.observe(self.on.update_action, self._on_update_action)

        for relation in self.meta.relations:
            on_relation = self.on[relation]
            for evt in ['changed', 'created', 'joined']:
                self.framework.observe(getattr(on_relation, "relation_" + evt), self._on_update_relation)

    def _on_update_action(self, e: ops.ActionEvent):
        updated = []
        if endpoint := e.params.get("endpoint"):
            app_data = e.params.get("app_data", "")
            unit_data = e.params.get("unit_data", "")
            if app_data or unit_data:
                self._write_mock(
                    endpoint,
                    json.loads(app_data),
                    json.loads(unit_data)
                )

            e.log(f"updating endpoint {endpoint}")
            if relations := self.model.relations[endpoint]:
                updated = self._update(*relations)
            else:
                e.log(f"no bindings on {endpoint}")

        else:
            e.log(f"updating all endpoints")
            updated = self._update()
        e.set_results({"updated": updated})

    def _on_clear_action(self, e: ops.ActionEvent):
        updated = []
        if endpoint := e.params.get("endpoint"):
            e.log(f"clearing endpoint {endpoint}")
            if relations := self.model.relations[endpoint]:
                updated = self._update(*relations, clear=True)
            else:
                e.log(f"no bindings on {endpoint}")
        else:
            e.log(f"clearing all endpoints")
            updated = self._update(clear=True)
        e.set_results({"cleared": updated})

    def _on_update_relation(self, e: ops.RelationEvent):
        self._update(e.relation)

    def _update(self, *relation: ops.Relation,
                clear=False):
        to_update = list(relation) if relation else list(chain(*self.model.relations.values()))
        updated = []
        for relation in to_update:
            if self._update_relation(relation, clear=clear):
                updated.append(relation.name)
        return updated

    def _update_relation(self, relation: ops.Relation,
                         clear=False, replace=False):
        changed = False

        app_databag = relation.data[self.app]
        unit_databag = relation.data[self.unit]
        if replace or clear:
            if app_databag.keys():
                app_databag.clear()
                changed = True
            if unit_databag.keys():
                unit_databag.clear()
                changed = True

        if not clear:
            app_data, unit_data = self._load_mock(relation.name)
            if app_data and dict(app_databag) != app_data:
                app_databag.update(app_data)
                changed = True
            if unit_data and dict(unit_databag) != unit_data:
                unit_databag.update(unit_data)
                changed = True
        return changed

    def _load_mock(self, endpoint: str):
        mocks_root = Path(__file__).parent.parent / 'mocks'

        if endpoint.startswith("provide"):
            pth = mocks_root / "provide" / (endpoint + ".yaml")
        else:
            pth = mocks_root / "provide" / (endpoint + ".yaml")

        if not pth.exists():
            logger.error(f"mock not found for {endpoint} ({pth})")
            return {}, {}

        yml = yaml.safe_load(pth.read_text())
        app_data = yml.get("app_data", {})
        unit_data = yml.get("unit_data", {})
        return app_data, unit_data

    def _write_mock(self, endpoint: str,
                    app_data: Optional[dict] = None,
                    unit_data: Optional[dict] = None):
        mocks_root = Path(__file__).parent.parent / 'mocks'

        if endpoint.startswith("provide"):
            pth = mocks_root / "provide" / (endpoint + ".yaml")
        else:
            pth = mocks_root / "provide" / (endpoint + ".yaml")

        if not pth.exists():
            logger.error(f"mock not found for {endpoint}")
            return {}, {}

        yml = yaml.safe_load(pth.read_text())

        if app_data == {}:
            _app_data = {}
        else:
            _app_data = yml.get("app_data") or {}
            if app_data:
                _app_data.update(app_data)

        if unit_data == {}:
            _unit_data = {}
        else:
            _unit_data = yml.get("unit_data") or {}
            if unit_data:
                _unit_data.update(unit_data)

        logger.info(f"updating mock with {_app_data}, {_unit_data}")
        pth.write_text(
            yaml.safe_dump(
                {"app_data": _app_data,
                 "unit_data": _unit_data}
            )
        )

    def _on_collect_unit_status(self, e: ops.CollectStatusEvent):
        e.add_status(ActiveStatus("facade ready"))

    # target for jhack eval
    def set(self,
            endpoint: str,
            relation_id: Optional[int] = None,
            app_data: Optional[Dict[str, str]] = None,
            unit_data: Optional[Dict[str, str]] = None,
            ):
        # keep mocks in sync
        self._write_mock(endpoint, app_data, unit_data)

        rel = self.model.get_relation(endpoint, relation_id)

        if app_data:
            rel.data[self.app].update(app_data)
        elif app_data is not None:  # user passed {}
            rel.data[self.app].clear()

        if unit_data:
            rel.data[self.unit].update(unit_data)
        elif unit_data is not None:  # user passed {}
            rel.data[self.unit].clear()


if __name__ == "__main__":  # pragma: nocover
    ops.main(FacadeCharm)  # type: ignore
