This is a pytest plugin for writing charm-side interface tests. 
If your charm implements a relation interface, you might want to use the 'official' relation interface tester code to verify that your charm complies with the interface.

# Usage

Add to your charm a `tests/interfaces` folder.

Add to your `tox.ini`:
```ini
[testenv:interface]
description = Run interface tests
deps =
    pytest
    pytest_interface_tester  # TODO: publish
    -r{toxinidir}/requirements.txt
commands =
    pytest -v --tb native {[vars]tst_path}interfaces --log-cli-level=INFO -s {posargs}
```

Now you can add your tests in `tests/interfaces`, and you can use the `interface_tester` fixture we provide to write your tests. Some minimal examples:

from unittest.mock import patch

If you need to patch your charm for the tests to run, this is where you do it:

```python
from unittest.mock import patch
from interface_tester import InterfaceTester
from charm import MyCharm

def test_all_interfaces(interface_tester: InterfaceTester):
    with patch('charm.KubernetesAPI', lambda **unused: None):
      interface_tester.configure(charm_type=MyCharm)
      interface_tester.run()
```