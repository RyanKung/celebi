## Celebi - A lightweight Data Anaylize Platform for Time Series Data


## TL;DR

`Celebi` is a lightweight services for time-series data. Which is based on `jirachi`, a actor model based IO toolsets based on pulsar.

## Design


## APIs

* /data/<id>/
- Method: GET POST DELETE PUT

```POS
{
    'mapper': <str>,
    'name': <str>
}
```

* /datum/<id>/
- Method: GET POST DELETE PUT


## Commands

* List all avaiable tests

```
python -m tests -l --log-level DEBUG
```

Test labels may looks like

```
apis.data
apis.meta
core.multi_app
io.postgres.benchmark
io.postgres.postgres
io.postgres.queryset
io.remote.remote_wsgi
io.requests
```


* Run a specially testcase

```
python -m tests <testcase label> --log-level DEBUG
```
