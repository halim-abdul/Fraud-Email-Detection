from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support

def train_model(texts: list[str], labels: list[int]):
    model=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2),min_df=1)),
                    ("classifier",LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42))])
    return model.fit(texts,labels)

def evaluate(model,texts:list[str], labels:list[int]):
    prediction=model.predict(texts)
    p,r,f,_=precision_recall_fscore_support(labels,prediction,average="binary",zero_division=0)
    return {"precision":float(p),"recall":float(r),"f1":float(f)}
