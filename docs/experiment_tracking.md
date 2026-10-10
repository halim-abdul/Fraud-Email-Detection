# MLflow

Install training extras, then `python scripts/train.py --mlflow`. Runs are local unless `MLFLOW_TRACKING_URI` is configured. Demo uses training-set toy results; never present these as test accuracy. Before deployment, add reproducible dataset versions, experiment seed, temporal holdout and leakage checks; log confidential datasets only within approved storage.
