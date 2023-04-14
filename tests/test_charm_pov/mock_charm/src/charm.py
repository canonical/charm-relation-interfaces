# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from charms.traefik_k8s.v0.ingress import IngressPerAppRequirer
from ops import CharmBase, Framework

KubernetesServicePatch = None


class MyCharm(CharmBase):
    use_ingress = True

    def __init__(self, framework: Framework):
        super().__init__(framework)
        if self.use_ingress:
            self.ingress = IngressPerAppRequirer(self, host="com.com", port=42)
