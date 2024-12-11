# Facade charm

The facade charm is somewhat similar to the any-charm, but is less generic and has a sharper focus on relation data.

Usage:
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

Your interface isn't in `charm-relation-interfaces` or on charmhub (yet)? No problem.
Add it to `custom_interfaces.yaml`, and it shall be picked up when you `tox -e pack`.


## interface conflicts
The operator framework translates `"-"` to `"_"` when generating event names.
So if you have an endpoint called `foo-bar`, you'll listen to relation events like: `self.on.foo_bar_relation_changed`.

So if you have two endpoints, one called `foo-bar` and another called `foo_bar`, the operator framework will complain that the event is already defined.

It turns out, there are some conflicts of this kind. 
In this case, instead of generating `provides-foo-bar` and `provides-foo_bar`, our approach is to map `foo-bar` to `foo__bar`.

So the facade charm will have:

```yaml
provides:
  provides-foo__bar:
    interface: foo-bar
  provides-foo_bar:
    interface: foo_bar
```

And same for `requires`.

The list of such conflicts, and how they've been resolved, at the time of writing, is:

- `vault-kv & vault_kv` --> **vault__kv**
- `nginx-route & nginx_route` --> **nginx__route**
- `grafana-dashboard & grafana_dashboard` --> **grafana__dashboard**
- `tls-certificates & tls_certificates` --> **tls__certificates**


