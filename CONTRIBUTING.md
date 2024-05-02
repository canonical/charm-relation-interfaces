# Contributing

So you have defined a relation interface, and think it would be useful in other places than your
immediate charm? That's excellent! The workflow of contributing a new interface is lightweight and
simple, while defining what makes a good interface and agreeing on what it should entail is not.

To contribute a new interface specification, open a pull request containing:

- a new directory: `/interfaces/{your-interface-name}`. In it, there should be:
  - a `README.md` explaining the purpose of the interface and the protocol
  - a `schema.py` file containing [Pydantic](https://pydantic.dev/) models that specify the app and unit databag model for either side of the interface.
  - an `interface.yaml` file. See the template linked below for an explanation of what it is expected to include.

  - a `interface_tests` directory in which you can put Python files containing interface tests. [Read more about interface tests](./README_INTERFACE_TESTS.md)
- under `docs/`, the JSON schemas generated from the Pydantic schemas. You can use command `tox -e build-json-schemas` to generate them automatically. Do not edit those files manually.

To quickly get started, see the [template interface](https://github.com/canonical/charm-relation-interfaces/tree/main/interfaces/__template__/v0) for a template of what to include and how it should be structured.

