# Interface tests

Charm relation interfaces are information exchange protocols for Juju charms.
In this repository, under each interface specification, it is possible to store a list of interface tests. The interface maintainers will write and maintain those tests for the interfaces they own. 
The goal of the tests is to provide an as strict as possible set of rules to determine whether a given charm satisfies that interface protocol.

For example, (simplifying a bit) the `ingress` protocol implemented by e.g. Traefik prescribes:
- on `ingress-relation-joined`, the requirer should write its part of the data to the relation. 
- on `ingress-relation-changed`, if the requirer has written its part of the data to the relation, then the provider should publish its part of the data. 


# Writing interface tests as an interface author
To write interface tests, we use [Scenario](https://github.com/canonical/ops-scenario). It is straightforward to translate the statements above to scenario tests:

> on `ingress-relation-joined`, the requirer should write its part of the data to the relation.

this becomes:

```python
from scenario import State, Relation

# from the POV of the requirer:
ingress = Relation('ingress')
state_out = State(relations=[ingress]).trigger(ingress.joined_event, ...)
assert state_out.get_relations('ingress')[0].local_app_data  # not empty
```
> on `ingress-relation-changed`, if the requirer has written its part of the data to the relation, then the provider should publish its part of the data. 
> 
```python
from scenario import State, Relation

# from the POV of the provider:
ingress = Relation(
    'ingress',
    remote_app_data={"data": "foo"}  # whatever data the provider expects to be supplied
)
state_out = State(relations=[ingress]).trigger(ingress.joined_event, ...)
assert state_out.get_relations('ingress')[0].local_app_data  # not empty

# and: 
ingress = Relation(
    'ingress', # the requirer has not sent its side of the data!
)
state_out = State(relations=[ingress]).trigger(ingress.joined_event, ...)
assert not state_out.get_relations('ingress')[0].local_app_data  # empty! 
```

Therefore, each relation interface specification translates to two sets of tests: some are meant for the requirer, some for the provider. 

In order to add interface tests to a charm relation interface `"my-interface"`, you should commit to this repository one or more python files under `repo-root/interfaces/my-interface/v0/interface_tests/`; for example:
`repo-root/interfaces/my-interface/v0/interface_tests/requirer_tests.py` and `repo-root/interfaces/my-interface/v0/interface_tests/provider_tests.py`.

Any python file in that directory will be scraped for tests. A test is any function decorated with the `interface_tester.interface_test_case` decorator.
Before you start writing interface tests, it's a good idea to pip install [interface-tester-pytest](https://github.com/canonical/interface-tester-pytest).
That will give you the right type hints as you're typing the code, and will also give you a little utility cli to verify that the tests you are writing are being correctly picked up by the same code that will eventually be used to run them.

## Your first interface test
You just created `repo-root/interfaces/my-interface/v0/interface_tests/requirer_tests.py`; let's write into it:

```python
from interface_tester import interface_test_case
from scenario import State,Network

@interface_test_case(
    # declare which role of the interface this test is meant to verify.
    role='requirer',

    # declare which event this test is about.
    event='my-interface-relation-joined',

    # you can override INPUT_STATE to provide a 'template' for the test case to build upon.
    #  99% of the time you won't need this: the test runner will inject for you a relation object
    #  matching the spec found in the charm-under-test's metadata.yaml.

    # However, suppose, if this relation interface requires a specific network binding
    #  in order to function, you could:
    input_state=State(
        networks=[
            Network(
                name='my-network',
                bind_addresses=[],
                ingress_addresses=[],
                egress_subnets=["1.1.1.42/42"]
            )
        ]
    )
)
def verify_output_state(output_state: State):
    # here: write assertion code that checks that, if the charm implementing the provider side were
    #  to receive an my-interface-relation-joined with that state, the charm would *do the right thing*,
    #  whatever that means in the context of this interface.
    #  for example, if the charm is meant to set application data as a response to this event, you could do:
    assert output_state.relations[0].local_app_data['baz'] == 'qux'
    # and if, say, the charm is meant to set unit status to ActiveStatus('foo') (or whatever):
    assert output_state.status.unit == 'active', 'foo'
```

Now, if you run `interface_tester discover` in a shell (in the repo root; or check out `--help` to see how to customize that), you should see something like:
```yaml
my-interface:
  - v0:
      - requirer:
          - verify_output_state:: my-interface-relation-joined (state=yes, schema=default)
```

This means that the test you just added is being collected. `state` indicates the presence of a custom `input_state` (which we did pass in the example above). `schema` indicates the type of schema validation to be performed.
Interface tests work closely together with the pydantic schemas supplied in `repo-root/interfaces/my-interface/v0/schema.py`. 

`interface_tester.interface_test_case` accepts a `schema` argument that can have one of four possible values:
- `interface_tester.interface_test.SchemaConfig.default` (or the string`"default"`): validate any `ingress` relation found in the `state_out` against the schema found in `schema.py`. If this interface test case is for the requirer, it will use the `RequirerSchema`; otherwise the `ProviderSchema`.
- `interface_tester.interface_test.SchemaConfig.skip` (or the string`"skip"`): skip schema validation for this test; use sparingly.
- `interface_tester.interface_test.SchemaConfig.empty` (or the string`"empty"`): assert that any `ingress` relation found in the `state_out` has **no relation data** at all (local side).
- you can pass a custom `interface_tester.schema_base.DataBagSchema` subclass, which will be used to validate any `ingress` relation found in `state_out`. This will replace the default one found in `schema.py` for this test only.

## Steps of an interface test
An interface test such as the one above has three steps:

- verify that the scenario runs
- verify that the output state (`state_out`) is valid (by the test-writer's definition)
- validate against the relation schemas

Failure in any of the three steps means a failed test.

# Matrix-testing interface compliance
Suppose we have an interface `foo`, with:
- `charms.yaml` listing 2 providers and 2 requirers of the `foo` interface.
- `schema.py` detailing the interface schema (optional: schema validation will be skipped if not found)
- `interface_tests/*.py` providing a list of interface tests for both roles

You can then run `python ./run_matrix.py foo`.
This will attempt to run the interface tests on all charms in `foo/charms.yaml`.
Omitting the `foo` argument will run the tests for all interfaces (warning: might take some time.)

# Using interface tests as a charm author
If you are the owner of a charm, and you are interested in adding your charm to an interface's `charms.yaml` (and thereby 'prove' that your charm complies with a given relation interface specification), then you need to follow the steps detailed at [interface-tester-pytest](https://github.com/canonical/interface-tester-pytest).