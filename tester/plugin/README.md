In order to automatically test the compliance of a charm with a relation interface specification defined in this repository, there are two main components that come together:
- interface tests: a battery of [scenario-based tests](https://github.com/PietroPasotti/ops-scenario/blob/main/README.md) that verify as comprehensively as possible whether any given charm's behaviour conforms to the interface specification.
- the `pytest-interface-tester` plugin: a pytest fixture to facilitate running the interface tests using the scenario API. The plugin can be used by: 
  - this repo's automation to verify that the charms registered with a given interface's `charms.yaml` listing do in fact conform to the specification.
  - charm authors, to verify (during development) or in their own CIs that the charm satisfies a given relation interface specification (whether the charm is registered in the interface's `charms.yaml` or not).

# How to write interface tests
- You can start by copying the template at `interfaces/__template__/interface_tests/interface_tests.py` to `interfaces/your-interface-name/interface_tests/interface_tests.py` (the filename is up to you, there can be multiple files)
- Run `tester/collect_interface_tests.py` to verify that the file you just added is discovered. You should see: 
    ```yaml
    your-interface-name:  # e.g. "database"
      - versionID:        # e.g. "v0"
        - requirer:
           - MyInterfaceRequirerChangedTest:: interface-name-relation-created (state=yes)
           - schema NOT OK  # unless you already added a schema in `interfaces/your-interface-name/schema.py`
           - <no charms>  # unless you already added some charms in `interfaces/your-interface-name/charms.yaml`
        - provider:
           - MyInterfaceProviderCreatedTest:: interface-name-relation-changed (state=no)
           - schema NOT OK  # ditto
           - <no charms>    # ditto
    ```
- Fill in the tests with whatever is appropriate. Feel free to add as many requirer/provider tests as you need, and if necessary, split them over multiple files. 
- All modules in `interfaces/your-interface-name/interface_tests/` will be loaded and all files will be scraped for functions marked with the `interface_test_case` decorator. All valid tests will be displayed in the listing: if a test you added didn't show up, it's not valid for some reason (e.g. you forgot to add the decorator, or to give the mandatory `state_out` positional argument to your callable). 


# the pytest-interface-tester plugin
This repo contains a python package for a pytest plugin called `pytest-interface-tester`. 

This plugin has two distinct purposes:
- it allows charm authors to expose a custom facade for the charm to be scraped by the [charm-relation-interfaces](https://github.com/canonical/charm-relation-interfaces) automated tester.
  If your charm needs some patching/mocking/config in order for it to run with [scenario](https://github.com/PietroPasotti/ops-scenario), 
- it allows charm authors to add relation interface tests to their charms (and, for example, wire it up with your testing automation).
  This means that you can test that your charm satisfies the spec of one or more relation interfaces, in exactly the same way as the charm-relation-interfaces automated tester is going to. 

After installing the plugin via `pip`, you can use the fixture in your pytests.

## Exposing a patched charm facade
If your charm can run with Scenario all relation events without needing patching, you don't need to do this.
Most charms, however, do things that Scenario can't or won't wrap for you. For example, make a kubernetes API call, Popen calls, send http requests, etc... In order to let your charm be scraped by the charm-relation-interfaces automated tester, you need to set up your charm to hide away all that state Scenario won't cover.

If you want to expose a custom charm facade for the automated charm-relation-interfaces tester, you will have to provide a pytest fixture named `interface_tester` at the `/tests/interfaces/conftest.py` path.

### Facade config
You can customize name and location of the facade, but you will need to include that data when registering your charm with the interface. In `charms.yaml`, you can then specify:
```yaml
  - name: my-charm-name  # required
    url: https://github.com/foo/my-charm-name  # required
    test_setup:  # optional
      location: path/to/file.py  # optional; default = tests/interfaces/conftest.py
      identifier: my_fixture_name # optional; default = interface_tester
```


Your `/tests/interfaces/conftest.py` should minimally contain:
```python
import pytest
from pytest_interface_tester import InterfaceTester
from charm import MyCharmName

@pytest.fixture
def interface_tester(interface_tester: InterfaceTester):
    # this is to tell to the automated tester which charm class it should use:
    interface_tester.configure(charm_type=MyCharmName)  
    yield interface_tester
```

If you want to patch your charm in any way, this is where you should do it. For example:

```python
import pytest
from pytest_interface_tester import InterfaceTester
from charm import MyCharmName
from unittest.mock import patch

@pytest.fixture
def interface_tester(interface_tester: InterfaceTester):
    with patch("charm.KubernetesServicePatch", lambda **unused: None):
        MyCharmName.some_method = lambda self: 42
        interface_tester.configure(charm_type=MyCharmName)  
        yield interface_tester
```

## Testing locally the interfaces
A minimal example of a test for the ingress interface is:

```python
from pytest_interface_tester import InterfaceTester
from charm import MyCharm

def test_ingress_interface(interface_tester: InterfaceTester):
    interface_tester.configure(charm_type=MyCharm, interface_name='ingress')
    interface_tester.run()
```

If you provide a custom facade for your charm, you will most likely need to use it in the local interface tests as well. In that case, the test will look like:

```python
from pytest_interface_tester import InterfaceTester
from charm import MyCharm

def test_ingress_interface(interface_tester: InterfaceTester):
    interface_tester.configure(charm_type=MyCharm, interface_name='ingress')
    interface_tester.run()
```

