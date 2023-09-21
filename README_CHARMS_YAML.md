Each version of each interface listed in this repository is expected to contain a `charms.yaml` file, listing the reference charms implementing it.

The format of the file is:

```yaml
# (Mandatory) List of requirer charms (and optionally their test configs)
requirers: 

  # (Mandatory) name of the charm, same as what is listed in its charmcraft.yaml
  # example: grafana-k8s
  - name: <charm-name>

    # (Mandatory) url of a git repo at which the charm source code can be found
    # example: https://github.com/canonical/grafana-k8s-operator
    url: <git repository url>

    # (Optional): Configuration for the test runner. It tells the interface test 
    # runner how to set up the context for the charm to be testable under the 
    # conditions required by this repository. Necessary if the charm requires, 
    # for example, a specific config, leadership, container connectivity, etc... in 
    # order to process the relation events as requested in order to comply with 
    # the interface.
    # For more details, see the interface-tester-pytest documentation at:
    #   https://github.com/canonical/interface-tester-pytest
    test_setup:

      # (Optional)
      # name of a pytest fixture (a function) **yielding** a configured 
      # `interface_tester.InterfaceTester` object.
      # default: "interface_tester"
      identifier: <identifier> 
      
      # (Optional) path to the (conftest.py) python file containing the identifier
      # called <identifier>. Path is relative to the root of 
      # the charm repository as specified in `url` above.
      # default: tests/interface/conftest.py
      location: path/to/file.py

# (Mandatory) List of provider charms (and optionally their test configs)
providers: [] # format is same as `requirers`
```