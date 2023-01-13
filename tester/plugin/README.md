=======================
pytest-interface-tester
=======================

This is a pytest plugin for adding relation interface tests to your charm.

The interface tests are [scenario-based tests](https://github.com/PietroPasotti/ops-scenario).

Examples:

```python
from interface_tester import InterfaceTester
from charm import MyCharm

def test_all_interfaces(interface_tester: InterfaceTester):
    interface_tester.configure(charm=MyCharm)
    interface_tester.run()  # will test all interfaces it can load from metadata.yaml

def test_ingress_interface(interface_tester: InterfaceTester):
    interface_tester.run(interface_name='ingress')
```