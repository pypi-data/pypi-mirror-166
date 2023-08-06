OIDC Client
===========

A pure-Python OpenID Connect client supporting OAuth 2.1 authorization flows, built for Python 3.10+ with minimal dependencies.

OAuth 2.1 authorization flows include:
- the **authorization code** flow, for interactive user login;
- the **client credentials** flow, for confidential machine-to-machine communication.

This OIDC Client supports reading configuration profiles from a `pyproject.toml` file.


Requirements
------------

Python 3.10+



Installation
------------

```console
pip install oidc-client
```


Examples
--------

```console
# To log-in as user, using a web browser:
oidc login --interactive
```

