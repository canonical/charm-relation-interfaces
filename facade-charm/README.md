# Facade charm

Usage:
`tox -e pack`
`juju deploy facade`
`juju relate facade:provide-your-interface <your charm>`

## update databags from jhack eval

`jhack eval facade/0 "self.set('provide-your-interface', app_data={'hello': 'world'}, unit_data={'lets foo': 'those bars')"`

## update databags from mock files

`cd facade-charm`
`jhack sync -S facade/0 --include-files=".*\.yaml" --source mocks`

`cd facade-charm/mocks/provide`

edit `provide-your-interface.yaml`

`juju run facade update`
