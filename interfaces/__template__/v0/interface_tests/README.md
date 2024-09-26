This directory is meant to contain the tests for your interface, so that it is possible to programmatically verify its implementations.

Find some relevant documentation at:
- [Interface Tests](https://discourse.charmhub.io/t/interface-tests/12691)
- [How to write interface tests](https://discourse.charmhub.io/t/how-to-write-interface-tests/12690)

## Quickstart

Copy this test to `test_provider.py` and fill in the blanks however appropriate for your interfaces

```python
from scenario import Relation, State
from scenario.context import CharmEvents
from interface_tester import Tester

def test_data_published_on_changed_remote_valid():
    # GIVEN a relation over <interface> containing all the right data 
    #  in the right format for the <requirer side>:
    relation = Relation(
        endpoint='ingress',
        interface='ingress', remote_app_name='remote',
        remote_app_data={'foo': '"bar"', 'baz': '42', 'qux': '"www.lol.com:4242"', },
        remote_units_data={0: {'fizz': 'buzz', }})
    t = Tester(
        State(relations=[relation])
    )
    
    # WHEN the <provider side> receives a <endpoint-changed-event> event:
    t.run(CharmEvents.relation_changed(relation))
    
    # THEN the <provider side> also publishes valid data to its side of the relation 
    #  (if applicable)
    t.assert_schema_valid()
```
