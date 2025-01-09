# Interface tests

Charm relation interfaces are information exchange protocols for Juju charms.
In this repository, under each interface specification, it is possible to store a list of interface tests. The interface maintainers will write and maintain those tests for the interfaces they own. 
The goal of the interface tests is to determine whether a given charm satisfies an interface protocol.

There are two personas that need to work with interface tests: interface authors and interface users.
If you are an interface user, i.e. the owner of a charm that uses some of the interfaces specified in this repository, then you should look at the documentation in the [interface-tester-pytest](https://github.com/canonical/interface-tester-pytest) repository.

If you are an interface author, this page is for you.

# How-To write interface tests as an interface author

Throughout this example we will write some interface tests for the `ingress` interface.
This is the expected behaviour for the interface:
1) on `ingress-relation-joined`, the requirer should write its part of the data to the relation. 
2) on `ingress-relation-changed`, if the provider has written its part of the data to the relation, then the provider should publish its part of the data; otherwise it should publish no data.

## A minimal test case

### Register a charm to the interface
Write to `./interfaces/ingress/v0/charms.yaml`:

```yaml
providers:
  - name: traefik-k8s
    url: https://github.com/canonical/traefik-k8s-operator

requirers: []
```

Verify that the [`charms.yaml` file format](README_CHARMS_YAML.md) is correct:

`interface_tester discover --include ingress`

You should see:

```text
collecting tests from root = /home/pietro/canonical/charm-relation-interfaces...
Discovered:
ingress:
  - v1:
   - provider:
     - <no tests>
     - schema NOT OK
     - charms:
       - traefik-k8s (https://github.com/canonical/traefik-k8s-operator) custom_test_setup=no
   - requirer:
     - <no tests>
     - schema NOT OK
     - <no charms>
```

### Add a relation interface schema
Install the [interface tester package](https://github.com/canonical/interface-tester-pytest):

`pip install interface-tester-pytest`

Specify the schema for the `ingress` interface databags in `./interfaces/ingress/v0/schema.py`, for example:

```python
from pydantic import BaseModel
from interface_tester import DataBagSchema

class MyRequirerUnitData(BaseModel):
    foo: str
    
class RequirerSchema(DataBagSchema):
    unit = MyRequirerUnitData()

class MyProviderAppData(BaseModel):
    bar: str
    baz: str
    
class ProviderSchema(DataBagSchema):
    app = MyProviderAppData()
```

Verify that the schemas are correctly specified:

`interface_tester discover --include ingress`

you should see:

```text
collecting tests from root = /home/pietro/canonical/charm-relation-interfaces...
Discovered:
ingress:
  - v1:
   - provider:
     - <no tests>
     - schema OK # schema found and valid
     - charms:
       - traefik-k8s (https://github.com/canonical/traefik-k8s-operator) custom_test_setup=no
   - requirer:
     - <no tests>
     - schema OK # schema found and valid
     - <no charms>
```

### Add interface tests
An interface test is any function named `test_*` that we can find in either file: 
- `<repo-root>/interfaces/ingress/v0/interface_tests/test_provider.py`
- `<repo-root>/interfaces/ingress/v0/interface_tests/test_requirer.py`

The name is important!

Create a python file at `<repo-root>/interfaces/ingress/v0/interface_tests/test_requirer.py` with this content:

```python
from scenario import State
from interface_tester import Tester

def test_data_published_on_joined():
    t = Tester(State())
    t.run("ingress-relation-joined")
    t.assert_relation_data_empty()
```

Verify that the tests are specified correctly:

`interface_tester discover --include ingress`

You should see:

```text
collecting tests from root = /home/pietro/canonical/charm-relation-interfaces...
Discovered:
ingress:
  - v1:
   - provider:
     - <no tests>
     - schema OK
     - charms:
       - traefik-k8s (https://github.com/canonical/traefik-k8s-operator) custom_test_setup=no
   - requirer:
      - test_data_published_on_joined
     - schema OK
     - <no charms>
```


Run the test: 

`python run_matrix.py --include ingress`

You should see:

```json
{
  "ingress": {
    "v0": {
      "provider": {},
      "requirer": {
        "my-charm": true
      }
    }
  }
}

```


## Validating the output state

If the specification dictates something more than "the databag contents should match this schema in that event", for example:

> on `ingress-relation-joined`, the requirer should write its part of the data to the relation and set its status to Active.

The test would then become:

```python
from scenario import State
from interface_tester import Tester


def test_data_published_on_joined():
    t = Tester()
    state_out: State = t.run("ingress-relation-joined")
    t.assert_relation_data_empty()
    
    assert state_out.unit_status.name == 'active'
```


## Testing a negative

The second norm we have above contains a negative. We split it into two assertions to write the tests:

> on `ingress-relation-changed`, if the requirer has provided 'data' and 'baz' information in its relation databags, then the provider should publish its part of the data.
> on `ingress-relation-changed`, if the requirer has NOT provided 'data' and 'baz' information in its relation databags, then the provider should publish no data.

This becomes two test cases:

```python
from scenario import State, Relation
from interface_tester import Tester


def test_data_published_on_joined_if_remote_has_sent_valid_data(output_state: State):
    """If the requirer has provided correct data, then the provider will populate its side of the databag."""

    t = Tester(State(
        relations=[Relation(
            endpoint='foo',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'data': 'foo-bar',
                'baz': 'qux'
            }
        )]
    ))
    state_out: State = t.run("ingress-relation-joined")
    t.assert_schema_valid()
    
    assert state_out.unit_status.name == 'blocked'

def test_no_data_published_on_joined_if_remote_has_not_sent_valid_data():
    """If the requirer has provided INcorrect data, then the provider will not write anything to its databags."""
    t = Tester(State(
        relations=[Relation(
            endpoint='foo',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'some': 'rubbish'
            }
        )]
    ))
    state_out: State = t.run("ingress-relation-joined")
    t.assert_relation_data_empty()
    
    assert state_out.unit_status.name == 'blocked'

```

Note the usage of `assert_relation_data_empty/assert_schema_valid`. Within the scope of an interface test you must call one of the two (or disable schema checking altogether with `skip_schema_validation`).


# Reference: how does it work?
Each interface test maps to a [Scenario test](https://github.com/canonical/ops-scenario).

The arguments passed to `Tester`, along with metadata gathered from the charm being tested, are used to assemble a scenario test. Once that is done, each interface test can be broken down in three steps, each one verifying separate things in order:

- verify that the scenario test runs (i.e. it can produce an output state without the charm raising exceptions)
- verify that the output state is valid (by the interface-test-writer's definition): i.e. that the test function returns without raising any exception
- validate the local relation databags against the role's relation schema provided in `schema.py` (or against a custom schema)

If any of these steps fail, the test as a whole is considered failed.


## Configuring the schema to be used in an interface test
Interface tests work closely together with the `RequirerSchema|ProviderSchema` pydantic models supplied in `repo-root/interfaces/ingress/v0/schema.py`.
If your interface has a `schema.py`, you can check whether the schema is specified correctly or not by running `interface_tester discover`. You should see:

```yaml
ingress:
  - v0:
      - requirer:
          - tests:
              <...>
          - schema: OK
```

If it says `NOT OK`, there is an error in the schema format or the filename.

### Referencing the schema in an interface test
When you write an interface test for `ingress`, by default, the test case will validate the relation against the schema provider in `schema.py` (using the appropriate role).
In more complex cases, e.g. if the schema can assume one of multiple shapes depending on the position in a sequence of data exchanges, it can be handy to override that default.

`Tester.assert_schema_valid` accepts a `schema` argument that allows you to configure the expected schema.
Pass to it a custom `interface_tester.DataBagSchema` subclass and that will replace the default schema for this test.

# Matrix-testing interface compliance
If we have:
- a `../interfaces/ingress/v0/charms.yaml` listing some providers and some requirers of the `ingress` interface.
- a `../interfaces/ingress/v0/schema.py` specifying the interface schema (optional: schema validation will be skipped if not found)
- two `../interfaces/ingress/v0/interface_tests/test_[requirer|provider].py` files providing a list of interface tests for either role

You can then run `python ./run_matrix.py ingress`.
This will attempt to run the interface tests on all charms in `.../interfaces/ingress/v0/charms.yaml`.
Omitting the `ingress` argument will run the tests for all interfaces (warning: might take some time.)

# Charm repo configuration
When developing the tests, it can be useful to run them against a specific branch of a charm repo. To do that, write in `charms.yaml`:

```yaml
providers:
  - name: traefik-k8s
    url: https://github.com/canonical/traefik-k8s-operator
    branch: develop  # any custom branch

requirers: []
```

Also it can be useful to configure where, relative to the repo root, the tester fixture can be found and what it is called.

```yaml
providers:
  - name: traefik-k8s
    url: https://github.com/canonical/traefik-k8s-operator
    test_setup: 
        location: foo/bar/baz.py  # location of the identifier
        identifier: qux  # name of a pytest fixture yielding a configured InterfaceTester

requirers: []
```
