from scenario import State
from interface_tester import Tester

def test_data_published_on_joined():
    t = Tester(State())
    t.run("database-relation-joined")
    t.assert_relation_data_empty()

