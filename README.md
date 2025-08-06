<div align="center">

  <h1>
    Charm Relation Interfaces
  </h1>
  <small>
    A catalogue of opinionated and standardized interface specifications for charmed operator relations.
  </small>
  </br></br>
  <p>
    <a href="https://matrix.to/#/#charmhub-integrations:ubuntu.com">
      <img src="https://img.shields.io/badge/Join%20us%20on%20Matrix-%23charmhub--integrations%3Aubuntu.com-blue" alt="Matrix badge" />
    </a>
  </p>
</div>

## Purpose
The purpose of the repository is to outline the behavior and requirements for key interface names, ensuring that charms claiming to implement a certain interface actually are capable of being integrated with each other.

## Contributing
[Contributing a new interface specification is a lightweight process](./CONTRIBUTING.md).

## Interfaces

For the time being, to see available interfaces, their statuses, and schemas, browse the [interfaces directory](./interfaces).

# Relation interface testers

In order to automatically validate whether a charm satisfies a given relation interface, the relation interface maintainer(s) need to write one or more **relation interface tests**. A relation interface test is a [scenario-based test case](https://documentation.ubuntu.com/ops/latest/howto/manage-interfaces/#write-tests-for-an-interface) which checks that, given an initial context, when a relation event is triggered, the charm will do what the interface specifies. For example, most interface testers will check that, on relation changed, the charm will write a certain value into its (app/unit) databag and that that value matches a certain (Pydantic) schema.

See [the tester documentation](https://github.com/canonical/interface-tester-pytest) for more.
