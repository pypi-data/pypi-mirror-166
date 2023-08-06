<h1 align="center">TCObservabilty</h1>
<h4 align="center">
    This lib was created to easily add observability to cloud functions using   opentelemetry
</h4>
<br>

---
## Pip Install

Run this command to intall:
```sh
pip install tcobservability
```
<br>

---
## Requirements

Before use that, make sure the cloud function has access to the following environments variables.

```sh
ENVIRONMENT="prod" #It can be hml, preprod or dev too.
OTEL_EXPORTER_ENDPOINT="{OTEL_EXPORTER_ENDPOINT}"
OTEL_EXPORTER_HEADERS_AUTH="{OTEL_EXPORTER_ENDPOINT}"
```

Obs.: These secrets are available on Google Cloud Secrets in the project B2B-data-PRD

Obs2.: If the `ENVIRONMENT` is `dev`, the logs will be printed on the terminal and not sent to the database, it's for tests.

<br>

---
## How to use


```py
from TCObservability.tracing import Trace

def main:
    # Starting the tracer
    tracer = Trace("{SERVICE NAME}").get_tracer()

    # Naming a trace
    with tracer.start_as_current_span(
        "{TRACER NAME}"
    ):
        YOUR CODE ...
```

## Instruments

The instruments are functions to automatically  get loggers from popular Python libraries. 

### Requests Instrument
```py
from TCObservability.tracing import TraceInstruments

TraceInstruments.start_requests_instrumentation()
```

### URLLib Instrument
```py
from TCObservability.tracing import TraceInstruments

TraceInstruments.start_urllib_instrumentation()
```
