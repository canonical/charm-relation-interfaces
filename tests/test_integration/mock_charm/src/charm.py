# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from charms.traefik_k8s.v1.ingress import IngressPerAppProvider
from ops import CharmBase, Framework

KubernetesServicePatch = None


class MyCharm(CharmBase):
    """Minimal charm providing ingress."""

    use_ingress = True

    def __init__(self, framework: Framework):
        super().__init__(framework)
        if self.use_ingress:
            ipa = IngressPerAppProvider(self)
            if ingress_relations := self.model.relations["ingress"]:
                ready = [
                    relation for relation in ingress_relations if ipa.is_ready(relation)
                ]
                for relation in ready:
                    ipa.publish_url(relation, "http://foo.com")
