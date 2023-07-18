# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the kubeflow-dashboard-sidebar interface.

Examples:
    RequirerSchema:
        unit: <empty>
        app: [
                {
                    "text": "some link text",
                    "link": "/some-link",
                    "type": "item",
                    "icon": "book"
                }
            ]
"""
from typing import List
import yaml
from pydantic import BaseModel, AnyHttpUrl, validator

from interface_tester.schema_base import DataBagSchema


class SidebarItem(BaseModel):
    """Representation of a Kubeflow Dashboard sidebar entry.

    See https://www.kubeflow.org/docs/components/central-dash/customizing-menu/ for more details.

    Args:
        text: The text shown in the sidebar
        link: The relative link within the host (eg: /runs, not http://.../runs)
        type: A type of sidebar entry (typically, "item")
        icon: An icon for the link, from
              https://kevingleason.me/Polymer-Todo/bower_components/iron-icons/demo/index.html
    """

    text: str
    link: str
    type: str  # noqa: A003
    icon: str


class RequirerSchema(DataBagSchema):
    """Requirer schema for Ingress."""

    app: List[SidebarItem]
