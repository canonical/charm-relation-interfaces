# Interface tests

Charm relation interfaces are information exchange protocols for Juju charms.
In this repository, under each interface specification, it is possible to store a list of interface tests. The interface maintainers will write and maintain those tests for the interfaces they own. 
The goal of the interface tests is to determine whether a given charm satisfies an interface protocol.

There are two personas that need to work with interface tests: interface authors and interface users.
If you are an interface user, i.e. the owner of a charm that uses some of the interfaces specified in this repository, then you should look at the documentation in the [interface-tester-pytest](https://github.com/canonical/interface-tester-pytest) repository.

If you are an interface author, this page is for you.

# How-To write interface tests as an interface author

Firstly, `pip install` [`interface-tester-pytest`](https://github.com/canonical/interface-tester-pytest).
That will give you the right type hints as you're typing the code, and will also give you a little utility cli to verify that the tests you are writing are being correctly picked up by the same code that will eventually be used to run them.

Throughout this example we will write some interface tests for the `ingress` interface.
This is the expected behaviour for the interface:
1) on `ingress-relation-joined`, the requirer should write its part of the data to the relation. 
2) on `ingress-relation-changed`, if the provider has written its part of the data to the relation, then the provider should publish its part of the data; otherwise it should publish no data.

## A minimal test case

Specify the schema for the `ingress` interface databags in `./interfaces/ingress/v0/schema.py`.

Create a python file at `<repo-root>/interfaces/ingress/v0/interface_tests/my_tests.py` with these contents:

```python
from scenario import State
from interface_tester.interface_test import interface_test_case


@interface_test_case(
    event='ingress-relation-joined',
    role='requirer',
)
def test_data_published_on_joined(output_state: State):
    return
```

This is a complete interface test.

## Validating the output state

If the specification dictates something more than "the databag contents should match this schema in that event", for example:

> on `ingress-relation-joined`, the requirer should write its part of the data to the relation and set its status to Active.

The test would then become:

```python
from scenario import State
from interface_tester.interface_test import interface_test_case


@interface_test_case(
    event='ingress-relation-joined',
    role='requirer',
)
def test_data_published_on_joined(output_state: State):
    assert output_state.status.unit.name == 'active'
```


## Testing a negative

The second norm we have above contains a negative. We split it into two assertions to write the tests:

> on `ingress-relation-changed`, if the requirer has provided 'data' and 'baz' information in its relation databags, then the provider should publish its part of the data.
> on `ingress-relation-changed`, if the requirer has NOT provided 'data' and 'baz' information in its relation databags, then the provider should publish no data.

This becomes two test cases:

```python
from scenario import State, Relation
from interface_tester.interface_test import interface_test_case, SchemaConfig


@interface_test_case(
    event='ingress-relation-joined',
    role='provider',
    input_state=State(
        relations=[Relation(
            endpoint='foo',
            interface='ingress',
            remote_app_name='remote',  # this is our simulated requirer
            remote_app_data={
                'data': 'foo-bar',
                'baz': 'qux'
            }
        )]
    )
)
def test_data_published_on_joined_if_remote_has_sent_valid_data(output_state: State):
    pass

    
@interface_test_case(
    event='ingress-relation-joined',
    role='provider',
    schema=SchemaConfig.empty,
    input_state=State(
        relations=[Relation(
            endpoint='foo',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'some': 'rubbish'
            }
        )]
    )

)
def test_no_data_published_on_joined_if_remote_has_not_sent_valid_data(output_state: State):
    pass
```

The first test verifies that, if the requirer has provided correct data, then the provider will populate its side of the databag.
The second test verifies the negative side of the norm.
Note the usage of `SchemaConfig.empty`. That is what disables the 'default' schema validation and instructs the test runner to verify that the provider-side databags are empty instead of containing whatever they should contain according to `schema.py`.  


## Verifying the test is discoverable

If you run `interface_tester discover` in a shell (in the repo root; or check out `--help` to see how to customize that), you should see something like a list of:
```yaml
my-interface:
  - v0:
      - requirer:
          - tests:
            - <test name>:: <event name>
          - schema: OK
          - charms:
              - <charm name> (<url>)
```

If you are adding tests to an interface, you should be able to see them listed under `tests`. 
If your interface has a `schema.py`, you can check whether the schema is specified correctly or not.
If your interface lists one or more charms in `charms.yaml`, you can verify here that the format is correct.


# Reference: how does it work?
Each interface test maps to a [Scenario test](https://github.com/canonical/ops-scenario).

The metadata passed to `interface_test_case`, along with metadata gathered from the charm being tested, is used to assemble a scenario test. Once that is done, each interface test can be broken down in three steps, each one verifying separate things in order:

- verify that the scenario test runs (i.e. it can produce an output state without the charm raising exceptions)
- verify that the output state is valid (by the interface-test-writer's definition)
- validate the local relation databags against the role's relation schema provided in `schema.py`

If any of these steps fail, the test as a whole is considered failed.


## Configuring the schema to be used in an interface test
This means that the test you just added is being collected. `state` indicates the presence of a custom `input_state` (which we did pass in the example above). `schema` indicates the type of schema validation to be performed.
Interface tests work closely together with the pydantic schemas supplied in `repo-root/interfaces/ingress/v0/schema.py`. 

`interface_tester.interface_test_case` accepts a `schema` argument that can have one of four possible values:
- `interface_tester.interface_test.SchemaConfig.default` (or the string`"default"`): validate any `ingress` relation found in the `state_out` against the schema found in `schema.py`. If this interface test case is for the requirer, it will use the `RequirerSchema`; otherwise the `ProviderSchema`.
- `interface_tester.interface_test.SchemaConfig.skip` (or the string`"skip"`): skip schema validation for this test; use sparingly.
- `interface_tester.interface_test.SchemaConfig.empty` (or the string`"empty"`): assert that any `ingress` relation found in the `state_out` has **no relation data** at all (local side).
- you can pass a custom `interface_tester.schema_base.DataBagSchema` subclass, which will be used to validate any `ingress` relation found in `state_out`. This will replace the default one found in `schema.py` for this test only.


# Matrix-testing interface compliance
If we have:
- a `../interfaces/ingress/v0/charms.yaml` listing some providers and some requirers of the `ingress` interface.
- a `../interfaces/ingress/v0/schema.py` specifying the interface schema (optional: schema validation will be skipped if not found)
- a `../interfaces/ingress/v0/interface_tests/my_tests.py` providing a list of interface tests for either role

You can then run `python ./run_matrix.py ingress`.
This will attempt to run the interface tests on all charms in `.../interfaces/ingress/v0/charms.yaml`.
Omitting the `ingress` argument will run the tests for all interfaces (warning: might take some time.)
