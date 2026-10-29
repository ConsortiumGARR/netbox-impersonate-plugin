# Contributing

Report bugs and propose changes through
[GitHub issues](https://github.com/ConsortiumGARR/netbox-impersonate-plugin/issues)
and pull requests.

## Running the tests

The tests run inside a NetBox checkout, against PostgreSQL and Redis, as in
`.github/workflows/ci.yaml`.

```bash
docker run -d --name nbimp-pg -p 5432:5432 -e POSTGRES_DB=netbox \
  -e POSTGRES_USER=netbox -e POSTGRES_PASSWORD=netbox postgres:16-alpine
docker run -d --name nbimp-redis -p 6379:6379 redis:7-alpine

git clone --depth 1 --branch v4.7.4 https://github.com/netbox-community/netbox.git
pip install -r netbox/requirements.txt -e .

cd netbox/netbox
PYTHONPATH=../.. NETBOX_CONFIGURATION=testing.configuration \
  python manage.py test netbox_impersonate_plugin.tests
```

Code is formatted with Black and linted with Ruff, see the pre-commit setup in the
README.

## Releasing

1. Bump `__version__` in `netbox_impersonate_plugin/__init__.py` and `version` in
   `pyproject.toml`.
2. Add the release to `CHANGELOG.md` and its NetBox range to `COMPATIBILITY.md`,
   matching `min_version` and `max_version` in the plugin config.
3. Tag the commit `vX.Y.Z`.
