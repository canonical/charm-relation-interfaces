# Facade charm

Usage:
`tox -e pack`
`juju deploy facade`
`juju integrate facade:provide-your-interface <your charm>`

## update databags with jhack eval

`jhack eval facade/0 "self.set('provide-your-interface', app_data={'hello': 'world'}, unit_data={'lets foo': 'those bars'})"`

## update databags with actions

```yaml
# in params.yaml
endpoint: provide-tempo_cluster
app_data: '{"foo":"bar"}'
unit_data: '{"foo":"baz"}'
```

`juju run facade/0 update --params params.yaml`

## update databags from mock files

`cd facade-charm`
`jhack sync -S facade/0 --include-files=".*\.yaml" --source mocks`

`cd facade-charm/mocks/provide`

edit `provide-your-interface.yaml`

`juju run facade update`

# using custom interfaces

Your interface isn't in charm-relation-interfaces (yet)? No problem.
Add it to `custom_interfaces.yaml`, and it shall be picked up when you `tox -e pack`.