import argparse
import os
import pandas as pd
from fraud_email.ml import train_model,evaluate

def main():
    p=argparse.ArgumentParser();p.add_argument("--data",default="data/synthetic_example.csv");p.add_argument("--mlflow",action="store_true");args=p.parse_args()
    data=pd.read_csv(args.data)
    texts=(data.subject.fillna("")+" "+data.body.fillna("")).tolist()
    labels=data.label.isin(["phishing","fraud"]).astype(int).tolist()
    if len(set(labels))!=2:raise ValueError("Need both positive and negative examples")
    model=train_model(texts,labels)
    metrics=evaluate(model,texts,labels)
    print("TRAINING-SET DEMONSTRATION ONLY; NOT VALIDATION:",metrics)
    if args.mlflow:
        import mlflow
        with mlflow.start_run(run_name="synthetic_demo"):
            mlflow.log_params({"vectorizer":"tfidf","classifier":"logistic_regression","dataset":"synthetic"})
            mlflow.log_metrics(metrics)
if __name__=="__main__":main()
