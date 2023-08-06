# Overview
This library contains useful wrappers around the Tonic.ai API.

## Usage

Instantiate the API wrapper using the following code:

```
from tonic_api.api import TonicApi

# Do not include trailing backslash in TONIC_URL
api = TonicApi(TONIC_URL, API_KEY)
```

Once instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.

```
TonicApi:
    get_workspace(workspace_id) => Workspace

Workspace:
    id => string
    name => string
    models => Model[]

    train(model_id) => new job ID
    get_trained_model_by_training_job_id(job_id) => TrainedModel (or None if training is not done)
    get_training_status_by_training_job_id(job_id) => TrainingJobStatus
    get_most_recent_trained_model_by_model_id => TrainedModel

    describe() => debugger helper for printing fields

Model:
    id => string
    name => string
    query => string
    parameters => {}
    encodings => {}

    describe() => debugger helper for printing fields

TrainedModel:
    id => string
    job_id => string
    model => Model

    sample(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided)
    sample_source(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided). Note: NOT randomized. Upper limit is limited to row count in source.

    get_numeric_columns() => string[]
    get_categorical_columns() => string[]

    describe() => debugger helper for printing fields

TrainingJobStatus:
    state => string
    error => string[] or None
    tasks => {}

    current_epoch_progress() => dict or None

    describe() => debugger helper for printing fields
```
