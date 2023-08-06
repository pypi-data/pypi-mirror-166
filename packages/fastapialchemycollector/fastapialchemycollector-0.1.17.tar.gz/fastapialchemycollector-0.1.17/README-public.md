# Metis FastAPI SQLAlchemy log collector

### About

This library logs the HTTP requests created by FastAPI and SQLAlchemy with the SQL commands they generate. The library
can also collect the execution plan for deeper analysis.

The log records stored in a local file. Future versions will allow saving the log records directly to log collectors
such as DataDog, Logz.io and Splunk.

The log can be analyzed using
our [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=Metis.dba-ai-vscode)

### Technical

This library uses [OpenTelemetry](https://pypi.org/project/opentelemetry-sdk/) to instrument both FastAPI and
SQLAlchemy.

Tested on python 3.8.9, FastAPI 0.78.0, SQLAlchemy 1.4.33, PostgreSQL 12 or higher.

### Instrumentation

Installation:

```bash
pip install fastapialchemycollector
```

Instrumentation:

* Configure the destination file name

* Configure logging the execution plan

By default the package only logs the SQL commands and the estimated execution plan (PlanCollectType.ESTIMATED).

The library:

1. Logs the estimated execution plan by running the SQL command using
    ```sql
    EXPLAIN ( VERBOSE, COSTS, SUMMARY, FORMAT JSON)
    ```
2. Runs the SQL command.

Logging the estimated plan has an impact on performances but usually, in a dev environment who doesn't run a large
number of SQL commands, the impact is very low, around 3%.

Warning! Do NOT run the code in Production! An environment variable should prevent the package from collecting the
estimated execution plan in Production.

The library can be configured using PlanCollectType.NONE to log only the SQL Commands while the execution plans,
estimated or actual, will be calculated later using our platform.

* Using Metis platform with Apikey:

```python
import os
from sqlalchemy import create_engine
from fastapi import FastAPI
from fastapialchemycollector import setup, MetisInstrumentor, PlanCollectType

# existing app initialization
app = FastAPI()
engine = create_engine(os.environ['DATABASE_URI'])

# To start collecting the logs:
instrumentation: MetisInstrumentor = setup('<SERVICE_NAME>',
                                           service_version='<SERVICE_VERSION>',
                                           plan_collection_option=PlanCollectType.ESTIMATED,
                                           dsn="<URL>",
                                           api_key='<API_KEY>')

instrumentation.instrument_app(app, engine)
```

* Using local file:

```python
import os
from sqlalchemy import create_engine
from fastapi import FastAPI
from fastapialchemycollector import setup, MetisInstrumentor, PlanCollectType

# existing app initialization
app = FastAPI()
engine = create_engine(os.environ['DATABASE_URI'])

# The default log file name is 'metis-log-collector.log. You can change the default name.
optional_log_file_name = 'new_file_name_of_sqlalchemy_logs.log'

# By default, the package logs the SQL commands and their execution plan.
# It can also be configured manually to collect only the SQL commands using PlanCollectType.NONE.
# We recommend collecting the estimated plan too.
optional_plan_collect_type = PlanCollectType.ESTIMATED

# To start collecting the logs:
instrumentation: MetisInstrumentor = setup('service-name',
                                           service_version='1.0.0',
                                           plan_collection_option=PlanCollectType.ESTIMATED,
                                           file_name=optional_log_file_name)

instrumentation.instrument_app(app, engine)
```


### Example of a log entry (might be changed in the future)

```json
{
  "logs": [
    {
      "_uuid": "0b3f9b86-c620-11ec-9d14-b276246b1dc9",
      "query": "SELECT booking.book.title AS booking_book_title \nFROM booking.book",
      "dbEngine": "postgresql",
      "date": "2022-04-27T11:49:07.161743",
      "plan": {
        "Plan": {
          "Node Type": "Seq Scan",
          "Parallel Aware": false,
          "Async Capable": false,
          "Relation Name": "book",
          "Schema": "booking",
          "Alias": "book",
          "Startup Cost": 0.0,
          "Total Cost": 1.17,
          "Plan Rows": 17,
          "Plan Width": 14,
          "Output": [
            "title"
          ],
          "Shared Hit Blocks": 0,
          "Shared Read Blocks": 0,
          "Shared Dirtied Blocks": 0,
          "Shared Written Blocks": 0,
          "Local Hit Blocks": 0,
          "Local Read Blocks": 0,
          "Local Dirtied Blocks": 0,
          "Local Written Blocks": 0,
          "Temp Read Blocks": 0,
          "Temp Written Blocks": 0
        },
        "Planning": {
          "Shared Hit Blocks": 0,
          "Shared Read Blocks": 0,
          "Shared Dirtied Blocks": 0,
          "Shared Written Blocks": 0,
          "Local Hit Blocks": 0,
          "Local Read Blocks": 0,
          "Local Dirtied Blocks": 0,
          "Local Written Blocks": 0,
          "Temp Read Blocks": 0,
          "Temp Written Blocks": 0
        },
        "Planning Time": 0.044
      }
    }
  ],
  "framework": "FastAPI",
  "path": "/",
  "operationType": "GET",
  "requestDuration": 210.35,
  "requestStatus": 200
}
```
