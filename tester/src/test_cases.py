# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
"""Utility module for reading test cases."""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DataBagContents:
    """DataBagContent holds databag contents for the unit and app of either a local or a remote."""

    unit: Dict[str, any] = field(default_factory=dict)
    app: Dict[str, any] = field(default_factory=dict)


@dataclass
class TestCase:
    """TestCase consists of a local DatabagContent (input) and a remote dito (expected output)."""

    local: DataBagContents
    remote: List[str]


@dataclass
class Tester:
    """Tester is the root object of a test run."""

    states: List[TestCase]

    def validate(self):
        """Validate whether the provided test run yaml is valid."""
        pass


def get_test_cases(source: Dict[str, List]) -> Tester:
    """Reads an arbitrary mass of text (source) and generates a collection of test cases."""
    tests = []
    for obj in source["states"]:
        test = TestCase(
            local=DataBagContents(
                app=obj["local"].get("app", {}),
                unit=obj["local"].get("unit", {}),
            ),
            remote=obj.get("remote", []),
        )
        tests.append(test)
    tester = Tester(tests)
    return tester
