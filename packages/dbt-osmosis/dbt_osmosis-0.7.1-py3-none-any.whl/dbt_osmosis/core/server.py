import decimal
import time
from functools import partial
from typing import Callable

import orjson
from bottle import JSONPlugin, install, request, response, route, run

from dbt_osmosis.core.osmosis import DbtOsmosis

JINJA_CH = ["{{", "}}", "{%", "%}"]


def default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def _dbt_query_engine(callback: Callable, runner: DbtOsmosis):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs, runner=runner)
        end = time.time()
        response.headers["X-dbt-Exec-Time"] = str(end - start)
        return body

    return wrapper


@route("/run", method="POST")
def run_sql(runner: DbtOsmosis):
    query = request.body.read().decode("utf-8")
    limit = request.query.get("limit", 200)
    if any(CH in query for CH in JINJA_CH):
        try:
            compiled_query = runner.compile_sql(query).compiled_sql
        except Exception as exc:
            return {"error": str(exc)}
    else:
        compiled_query = query

    query_with_limit = f"select * from ({compiled_query}) as osmosis_query limit {limit}"
    try:
        _, table = runner.execute_sql(query_with_limit, fetch=True)
    except Exception as exc:
        return {"error": str(exc)}

    return {
        "rows": [list(row) for row in table.rows],
        "column_names": table.column_names,
        "compiled_sql": compiled_query,
        "raw_sql": query,
    }


@route("/compile", method="POST")
def compile_sql(runner: DbtOsmosis):
    query = request.body.read().decode("utf-8")
    if any(CH in query for CH in JINJA_CH):
        try:
            compiled_query = runner.compile_sql(query).compiled_sql
        except Exception as exc:
            return {"error": str(exc)}
    else:
        compiled_query = query
    return {"result": compiled_query}


@route("/reset", method="POST")
def reset(runner: DbtOsmosis):
    try:
        runner.rebuild_dbt_manifest()
    except Exception as exc:
        return {"result": "failure", "error": str(exc)}
    else:
        return {"result": "success"}


def run_server(runner: DbtOsmosis, host="localhost", port=8581):
    dbt_query_engine = partial(_dbt_query_engine, runner=runner)
    install(dbt_query_engine)
    install(JSONPlugin(json_dumps=lambda body: orjson.dumps(body, default=default).decode("utf-8")))
    run(host=host, port=port)
