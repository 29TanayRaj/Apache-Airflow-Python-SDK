# Airflow Python SDK

A lightweight, robust, and asynchronous-friendly Python SDK for interacting with the **Apache Airflow v2 Stable REST API**.

This SDK follows a clean **Facade** and **Layered Architecture**, providing both Synchronous and Asynchronous clients to seamlessly manage your Airflow environments programmatically.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Airflow Configuration](#airflow-configuration)
- [Quick Start](#quick-start)
  - [Synchronous Client](#quick-start-synchronous)
  - [Asynchronous Client](#quick-start-asynchronous)
- [SDK Architecture](#sdk-architecture-overview)
- [Available Services & API Reference](#available-services--api-reference)
  - [DAGs](#dags---clientdags)
  - [DAG Runs](#dag-runs---clientdag_runs)
  - [Tasks](#tasks---clienttasks)
  - [Task Instances](#task-instances---clienttask_instances)
  - [DAG Sources](#dag-sources---clientdag_sources)
  - [DAG Stats](#dag-stats---clientdag_stats)
  - [DAG Versions](#dag-versions---clientdag_versions)
  - [DAG Warnings](#dag-warnings---clientdag_warnings)
  - [Variables](#variables---clientvariables)
  - [Connections](#connections---clientconnections)
  - [Pools](#pools---clientpools)
  - [Config](#config---clientconfig)
  - [Event Logs](#event-logs---clientevent_logs)
  - [Import Errors](#import-errors---clientimport_errors)
  - [Jobs](#jobs---clientjobs)
  - [Plugins](#plugins---clientplugins)
  - [Providers](#providers---clientproviders)
  - [Assets](#assets---clientassets)
  - [Backfills](#backfills---clientbackfills)
- [Request Models](#request-models)
- [Response Models](#response-models)
- [Error Handling](#error-handling)
- [Pagination](#pagination)
- [License](#license)

---

## Features

* **Full API Coverage** — Supports all Airflow v2 REST API endpoints: DAGs, DAG Runs, Tasks, Task Instances, Variables, Connections, Pools, Assets, Backfills, and more.
* **Dual Clients** — Provides both a synchronous `AirflowSDK` and an asynchronous `AsyncAirflowSDK`.
* **Layered Architecture** — Clean separation between the Facade, Domain Services, and Transport layers.
* **Resilience Built-In** — Automatic exponential backoff retries for common transient errors (e.g., 429 Rate Limits, 502/503/504 Server Errors).
* **Intuitive Exceptions** — Clear hierarchy of custom exceptions (`AirflowAuthError`, `AirflowRateLimitError`, `AirflowNotFoundError`, etc.).
* **Typed Response Models** — All responses are returned as Pydantic models for full IDE intellisense and type safety.
* **Context Manager Support** — Both clients fully support `with` / `async with` for automatic resource cleanup.

---

## Installation

Clone the repository and install in editable mode:

```bash
git clone <your-repo>/AirflowSDK
cd AirflowSDK
pip install -e .
```

---

## Requirements

| Dependency | Version |
|---|---|
| Python | 3.8+ |
| `httpx` | ≥ 0.24.0 |
| `anyio` | ≥ 3.0.0 |
| `pydantic` | ≥ 2.0.0 |

Install dependencies manually if needed:

```bash
pip install httpx anyio pydantic
```

---

## Airflow Configuration

Make sure your target Airflow environment has API authentication enabled. In `airflow.cfg`:

```ini
[api]
auth_backends = airflow.api.auth.backend.basic_auth
```

Restart Airflow after making changes:

```bash
airflow webserver restart
airflow scheduler restart
```

> **Tip:** For Airflow running via Docker Compose, set the environment variable `AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth`.

---

## Quick Start

### Quick Start: Synchronous

Use `AirflowSDK` as a context manager to ensure connections are properly closed.

```python
from src.sdk import AirflowSDK

with AirflowSDK(
    base_url="http://localhost:8080",
    username="admin",
    password="admin",
    retries=3       # optional, default is 3
) as client:

    # List all DAGs
    dag_collection = client.dags.list()
    print(f"Total DAGs: {dag_collection.total_entries}")
    for dag in dag_collection.dags:
        print(dag.dag_id, "| paused:", dag.is_paused)

    # Trigger a DAG Run
    run = client.dag_runs.trigger(
        dag_id="example_bash_operator",
        conf={"key": "value"}
    )
    print(f"Triggered run: {run.dag_run_id} | state: {run.state}")

    # Manage Variables
    client.variables.create(request=VariableCreateRequest(key="env", value="production"))
    var = client.variables.get("env")
    print(var.value)
```

You can also use the SDK without a context manager; just call `.close()` when done:

```python
client = AirflowSDK("http://localhost:8080", "admin", "admin")
dags = client.dags.list()
client.close()
```

---

### Quick Start: Asynchronous

For concurrent applications (FastAPI servers, async workers, etc.), use `AsyncAirflowSDK`.

```python
import asyncio
from src.async_sdk import AsyncAirflowSDK

async def main():
    async with AsyncAirflowSDK(
        base_url="http://localhost:8080",
        username="admin",
        password="admin"
    ) as client:

        # Fetch DAGs and config concurrently
        dags, config = await asyncio.gather(
            client.dags.list(),
            client.config.get_config()
        )

        print(f"Found {dags.total_entries} DAGs")
        print(f"Config sections: {len(config.sections)}")

        # Trigger a run asynchronously
        run = await client.dag_runs.trigger("my_dag", conf={"date": "2024-01-01"})
        print(f"State: {run.state}")

asyncio.run(main())
```

> **Note:** Every method on `AsyncAirflowSDK` services is a coroutine and must be awaited.

---

## SDK Architecture Overview

```
AirflowSDK / AsyncAirflowSDK        ← Facade Layer (entry point)
    │
    ├── client.dags                  ─┐
    ├── client.dag_runs               │
    ├── client.tasks                  │  Service Layer (src/services/)
    ├── client.task_instances         │  Domain-scoped API modules
    ├── client.variables              │  returning typed Pydantic models
    ├── client.connections            │
    ├── client.pools                  │
    ├── client.config                 │
    ├── client.assets                 │
    ├── client.backfills             ─┘
    │
    └── APIClient / AsyncAPIClient   ← Core Layer (src/core/)
            ├── httpx transport
            ├── Basic Auth
            └── Exponential backoff retry
```

**Layers:**

1. **Facade Layer** (`src/sdk.py`, `src/async_sdk.py`) — The primary entry point. Exposes all domain services as attributes (e.g., `client.dags`, `client.connections`).
2. **Service Layer** (`src/services/`) — Domain-specific modules that implement exact REST API logic and return typed Pydantic models.
3. **Core Layer** (`src/core/`) — Handles all HTTP transport, session state, authentication, and retry logic using `httpx`.

---

## Available Services & API Reference

All methods below apply equally to both `AirflowSDK` (sync) and `AsyncAirflowSDK` (async — prefix calls with `await`).

---

### DAGs — `client.dags`

Manage your Airflow DAG definitions.

| Method | Description |
|---|---|
| `list(limit, offset, tags)` | List all DAGs. Optionally filter by tags. |
| `get(dag_id)` | Get a specific DAG by ID. |
| `get_details(dag_id)` | Get detailed information about a DAG. |
| `patch(dag_id, update_mask, **kwargs)` | Update fields on a DAG. |
| `delete(dag_id)` | Delete a DAG. |
| `pause(dag_id, is_paused=True)` | Pause or unpause a DAG. |

**Examples:**

```python
# List first 50 DAGs
result = client.dags.list(limit=50, offset=0)
for dag in result.dags:
    print(dag.dag_id, dag.owners, dag.tags)

# Get a specific DAG
dag = client.dags.get("my_etl_dag")
print(dag.fileloc, dag.is_active)

# Pause a DAG
client.dags.pause("my_etl_dag")

# Unpause a DAG
client.dags.pause("my_etl_dag", is_paused=False)

# Delete a DAG
client.dags.delete("old_dag")

# Filter by tags
result = client.dags.list(tags=["production", "finance"])
```

---

### DAG Runs — `client.dag_runs`

Manage and monitor DAG run executions.

| Method | Description |
|---|---|
| `list(dag_id, limit, offset)` | List all runs for a DAG. |
| `get(dag_id, dag_run_id)` | Get a specific DAG run. |
| `trigger(dag_id, conf, logical_date)` | Trigger a new DAG run. |
| `delete(dag_id, dag_run_id)` | Delete a DAG run. |
| `clear(dag_id, dag_run_id, dry_run)` | Clear (re-run) a DAG run. |

**Examples:**

```python
# Trigger a DAG run with configuration
run = client.dag_runs.trigger(
    dag_id="my_dag",
    conf={"environment": "prod", "date": "2024-06-01"},
    logical_date="2024-06-01T00:00:00Z"  # optional
)
print(run.dag_run_id, run.state)   # e.g. "manual__2024-06-01" | "queued"

# List all runs for a DAG
runs = client.dag_runs.list("my_dag", limit=20)
for run in runs.dag_runs:
    print(run.dag_run_id, run.state, run.start_date)

# Get a specific run
run = client.dag_runs.get("my_dag", "manual__2024-06-01")

# Clear (retry) a failed run
client.dag_runs.clear("my_dag", "manual__2024-06-01", dry_run=False)

# Delete a run
client.dag_runs.delete("my_dag", "manual__2024-06-01")
```

---

### Tasks — `client.tasks`

Inspect task definitions within a DAG.

| Method | Description |
|---|---|
| `list(dag_id)` | List all tasks in a DAG. |
| `get(dag_id, task_id)` | Get a specific task definition. |

**Examples:**

```python
# List tasks in a DAG
tasks = client.tasks.list("my_dag")
for task in tasks.tasks:
    print(task.task_id, task.operator, task.downstream_task_ids)

# Get a specific task
task = client.tasks.get("my_dag", "process_data")
print(task.retries, task.pool, task.priority_weight)
```

---

### Task Instances — `client.task_instances`

Inspect individual task execution instances.

| Method | Description |
|---|---|
| `list(dag_id, dag_run_id, limit, offset)` | List task instances for a run. |
| `get(dag_id, dag_run_id, task_id)` | Get a specific task instance. |

**Examples:**

```python
# List all task instances in a run
instances = client.task_instances.list("my_dag", "manual__2024-06-01")
for ti in instances.task_instances:
    print(ti.task_id, ti.state, ti.duration)

# Get a specific task instance
ti = client.task_instances.get("my_dag", "manual__2024-06-01", "process_data")
print(ti.state, ti.start_date, ti.end_date, ti.try_number)
```

---

### DAG Sources — `client.dag_sources`

Retrieve the raw Python source code of a DAG file.

| Method | Description |
|---|---|
| `get(dag_id)` | Get the source code for a DAG. |

**Examples:**

```python
source = client.dag_sources.get("my_dag")
print(source.content)   # Raw Python source of the DAG file
```

---

### DAG Stats — `client.dag_stats`

Get run state statistics per DAG.

| Method | Description |
|---|---|
| `get(dag_ids)` | Get stats for one or more DAGs. |

**Examples:**

```python
stats = client.dag_stats.get(dag_ids=["my_dag", "other_dag"])
for dag_stat in stats.dag_stats:
    print(dag_stat.dag_id)
    for s in dag_stat.stats:
        print(f"  {s.state}: {s.count}")
```

---

### DAG Versions — `client.dag_versions`

Inspect version history of your DAGs.

| Method | Description |
|---|---|
| `list(dag_id, limit, offset)` | List all versions of a DAG. |
| `get(dag_id, version_number)` | Get a specific version. |

**Examples:**

```python
versions = client.dag_versions.list("my_dag")
for v in versions.dag_versions:
    print(v.version_number, v.created_at, v.bundle_name)

# Get a specific version
v = client.dag_versions.get("my_dag", 3)
```

---

### DAG Warnings — `client.dag_warnings`

Retrieve import or configuration warnings for DAGs.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all DAG warnings. |

**Examples:**

```python
warnings = client.dag_warnings.list()
for w in warnings.dag_warnings:
    print(w.dag_id, w.warning_type, w.message)
```

---

### Variables — `client.variables`

Manage Airflow Variables (key-value configuration store).

| Method | Description |
|---|---|
| `list(limit, offset)` | List all variables. |
| `get(variable_key)` | Get a variable by key. |
| `create(request)` | Create a new variable. |
| `patch(variable_key, update_mask, **kwargs)` | Update an existing variable. |
| `delete(variable_key)` | Delete a variable. |

**Examples:**

```python
from src.services.admin.admin_models import VariableCreateRequest

# Create a variable
client.variables.create(VariableCreateRequest(
    key="api_url",
    value="https://myapi.example.com",
    description="External API endpoint"
))

# Read a variable
var = client.variables.get("api_url")
print(var.key, var.value, var.description)

# Update a variable value
client.variables.patch("api_url", value="https://newapi.example.com")

# List all variables
all_vars = client.variables.list(limit=50)
for v in all_vars.variables:
    print(v.key, v.value)

# Delete a variable
client.variables.delete("api_url")
```

---

### Connections — `client.connections`

Manage Airflow Connections (secrets for external services).

| Method | Description |
|---|---|
| `list(limit, offset)` | List all connections. |
| `get(connection_id)` | Get a connection by ID. |
| `create(request)` | Create a new connection. |
| `patch(connection_id, update_mask, **kwargs)` | Update a connection. |
| `delete(connection_id)` | Delete a connection. |

**Examples:**

```python
from src.services.admin.admin_models import ConnectionCreateRequest

# Create a Postgres connection
client.connections.create(ConnectionCreateRequest(
    connection_id="my_postgres",
    conn_type="postgres",
    host="db.example.com",
    login="admin",
    password="secret",
    port=5432,
    schema="mydb"
))

# Get a connection
conn = client.connections.get("my_postgres")
print(conn.host, conn.port, conn.schema_)

# List all connections
conns = client.connections.list()
for c in conns.connections:
    print(c.connection_id, c.conn_type)

# Update host
client.connections.patch("my_postgres", host="newdb.example.com")

# Delete
client.connections.delete("my_postgres")
```

---

### Pools — `client.pools`

Manage Airflow task execution Pools to limit concurrency.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all pools. |
| `get(pool_name)` | Get a specific pool. |
| `create(request)` | Create a new pool. |
| `patch(pool_name, update_mask, **kwargs)` | Update a pool. |
| `delete(pool_name)` | Delete a pool. |

**Examples:**

```python
from src.services.admin.admin_models import PoolCreateRequest

# Create a pool
pool = client.pools.create(PoolCreateRequest(
    name="etl_pool",
    slots=5,
    description="Pool for ETL pipeline tasks"
))
print(pool.name, pool.slots, pool.open_slots)

# Get pool status
pool = client.pools.get("etl_pool")
print(f"Running: {pool.running_slots} | Queued: {pool.queued_slots} | Open: {pool.open_slots}")

# Update slot count
client.pools.patch("etl_pool", slots=10)

# Delete pool
client.pools.delete("etl_pool")
```

---

### Config — `client.config`

Read Airflow server configuration values.

| Method | Description |
|---|---|
| `get_config()` | Get the full Airflow config. |
| `get_value(section, option)` | Get a single config option. |

**Examples:**

```python
# Get full config
config = client.config.get_config()
for section in config.sections:
    print(f"[{section.name}]")
    for opt in section.options:
        print(f"  {opt.key} = {opt.value}")

# Get a single value
val = client.config.get_value("core", "dags_folder")
print(val)
```

---

### Event Logs — `client.event_logs`

Retrieve the Airflow audit event log.

| Method | Description |
|---|---|
| `list(limit, offset)` | List event log entries. |
| `get(event_log_id)` | Get a specific event log entry. |

**Examples:**

```python
logs = client.event_logs.list(limit=20)
for log in logs.get("event_logs", []):
    print(log)

# Get a specific log entry
entry = client.event_logs.get("12345")
```

---

### Import Errors — `client.import_errors`

Inspect DAG import errors from the Airflow scheduler.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all import errors. |
| `get(import_error_id)` | Get a specific import error. |

**Examples:**

```python
errors = client.import_errors.list()
for err in errors.get("import_errors", []):
    print(err)
```

---

### Jobs — `client.jobs`

List active Airflow Scheduler/Webserver jobs.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all active jobs. |

**Examples:**

```python
jobs = client.jobs.list()
print(jobs)
```

---

### Plugins — `client.plugins`

List installed Airflow plugins.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all plugins. |

**Examples:**

```python
plugins = client.plugins.list()
for plugin in plugins.plugins:
    print(plugin.name, plugin.source)
```

---

### Providers — `client.providers`

List installed Airflow provider packages.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all providers. |

**Examples:**

```python
providers = client.providers.list()
for p in providers.providers:
    print(p.package_name, p.version)
```

---

### Assets — `client.assets`

Work with Airflow Data Assets (dataset-driven scheduling).

| Method | Description |
|---|---|
| `list(limit, offset)` | List all assets. |
| `get(asset_id)` | Get a specific asset. |
| `events(limit, offset)` | List asset events. |

**Examples:**

```python
# List all assets
assets = client.assets.list()
for asset in assets.assets:
    print(asset.uri, asset.extra)

# Get a specific asset
asset = client.assets.get(42)

# List asset events
events = client.assets.events()
```

---

### Backfills — `client.backfills`

Create and manage historical DAG Backfill runs.

| Method | Description |
|---|---|
| `list(limit, offset)` | List all backfills. |
| `get(backfill_id)` | Get a specific backfill. |
| `create(dag_id, from_date, to_date, **kwargs)` | Create a new backfill. |
| `pause(backfill_id)` | Pause a running backfill. |
| `unpause(backfill_id)` | Resume a paused backfill. |
| `cancel(backfill_id)` | Cancel a backfill. |

**Examples:**

```python
# Create a backfill for a date range
backfill = client.backfills.create(
    dag_id="my_dag",
    from_date="2024-01-01T00:00:00Z",
    to_date="2024-03-31T23:59:59Z"
)
print(backfill.backfill_id, backfill.state)

# Pause a running backfill
client.backfills.pause(backfill.backfill_id)

# Resume it
client.backfills.unpause(backfill.backfill_id)

# Cancel entirely
client.backfills.cancel(backfill.backfill_id)
```

---

## Request Models

Several creation methods accept Pydantic request models for structured, validated inputs:

```python
from src.services.admin.admin_models import (
    VariableCreateRequest,
    ConnectionCreateRequest,
    PoolCreateRequest,
)

# Variable
req = VariableCreateRequest(key="my_key", value="my_value", description="optional")

# Connection
req = ConnectionCreateRequest(
    connection_id="my_s3",
    conn_type="aws",
    host="s3.amazonaws.com",
    login="access_key_id",
    password="secret_access_key"
)

# Pool
req = PoolCreateRequest(name="my_pool", slots=10, description="optional")
```

---

## Response Models

All SDK methods return **typed Pydantic models**. This provides full attribute access and IDE autocompletion.

### DAG Models (`src/services/dags/dags_models.py`)

| Model | Key Fields |
|---|---|
| `DagModel` | `dag_id`, `is_paused`, `is_active`, `fileloc`, `owners`, `tags` |
| `DagCollection` | `dags: List[DagModel]`, `total_entries: int` |
| `DagRunModel` | `dag_run_id`, `dag_id`, `state`, `run_type`, `conf`, `logical_date` |
| `DagRunCollection` | `dag_runs: List[DagRunModel]`, `total_entries: int` |
| `TaskModel` | `task_id`, `retries`, `pool`, `queue`, `downstream_task_ids` |
| `TaskCollection` | `tasks: List[TaskModel]`, `total_entries: int` |
| `TaskInstanceModel` | `task_id`, `dag_id`, `state`, `duration`, `try_number`, `operator` |
| `TaskInstanceCollection` | `task_instances: List[TaskInstanceModel]`, `total_entries: int` |
| `DagVersionModel` | `version_number`, `dag_id`, `bundle_name`, `created_at` |
| `DagWarningModel` | `dag_id`, `warning_type`, `message`, `timestamp` |

### Admin Models (`src/services/admin/admin_models.py`)

| Model | Key Fields |
|---|---|
| `VariableModel` | `key`, `value`, `description` |
| `ConnectionModel` | `connection_id`, `conn_type`, `host`, `login`, `port`, `schema_` |
| `PoolModel` | `name`, `slots`, `occupied_slots`, `running_slots`, `queued_slots`, `open_slots` |
| `ConfigModel` | `sections: List[ConfigSectionModel]` |
| `ProviderModel` | `package_name`, `description`, `version` |
| `PluginModel` | `name`, `source` |

---

## Error Handling

The SDK raises specific exceptions defined in `src/exceptions.py`. Catch them precisely for robust error management.

### Exception Hierarchy

```
AirflowAPIError                  ← Base exception
├── AirflowAuthError             ← 401 Unauthorized / 403 Forbidden
└── AirflowRequestError          ← Any HTTP error (has .status_code, .response_data)
    ├── AirflowRateLimitError    ← 429 Too Many Requests (auto-retried)
    └── AirflowNotFoundError     ← 404 Not Found
```

### Usage

```python
from src.sdk import AirflowSDK
from src.exceptions import (
    AirflowAuthError,
    AirflowNotFoundError,
    AirflowRateLimitError,
    AirflowRequestError,
    AirflowAPIError,
)

with AirflowSDK("http://localhost:8080", "admin", "admin") as client:
    try:
        dag = client.dags.get("non_existent_dag")

    except AirflowNotFoundError as e:
        print(f"DAG not found: {e}")
        print(f"HTTP Status: {e.status_code}")

    except AirflowAuthError:
        print("Authentication failed. Check username/password.")

    except AirflowRateLimitError:
        print("Rate limit hit. Request will be retried automatically.")

    except AirflowRequestError as e:
        print(f"HTTP error {e.status_code}: {e.response_data}")

    except AirflowAPIError as e:
        print(f"SDK error: {e}")
```

> **Tip:** `AirflowRateLimitError` (429) and server errors (502, 503, 504) are automatically retried with exponential backoff. The number of retries is controlled by the `retries` parameter in the SDK constructor (default: 3).

---

## Pagination

All collection endpoints support `limit` and `offset` for pagination. Responses include `total_entries` so you can calculate the total number of pages.

```python
PAGE_SIZE = 50

# Get first page
page1 = client.dags.list(limit=PAGE_SIZE, offset=0)
total = page1.total_entries
print(f"Page 1: Got {len(page1.dags)} of {total} total DAGs")

# Get second page
page2 = client.dags.list(limit=PAGE_SIZE, offset=PAGE_SIZE)

# Iterate through all pages
all_dags = []
offset = 0
while True:
    result = client.dags.list(limit=PAGE_SIZE, offset=offset)
    all_dags.extend(result.dags)
    offset += PAGE_SIZE
    if offset >= result.total_entries:
        break

print(f"Fetched all {len(all_dags)} DAGs")
```

---

## Async Concurrency Example

The async client is ideal for running many API calls in parallel:

```python
import asyncio
from src.async_sdk import AsyncAirflowSDK

async def monitor_dags(dag_ids: list):
    async with AsyncAirflowSDK("http://localhost:8080", "admin", "admin") as client:
        # Fetch details for multiple DAGs concurrently
        tasks = [client.dags.get(dag_id) for dag_id in dag_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for dag_id, result in zip(dag_ids, results):
            if isinstance(result, Exception):
                print(f"{dag_id}: ERROR — {result}")
            else:
                print(f"{dag_id}: paused={result.is_paused}, active={result.is_active}")

asyncio.run(monitor_dags(["dag_1", "dag_2", "dag_3"]))
```

---

## License

MIT License
