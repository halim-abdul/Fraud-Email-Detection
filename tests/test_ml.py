from fraud_email.ml import train_model,evaluate

def test_train_smoke():
    x=["office meeting today","win lottery money","meeting agenda","crypto send money"]
    y=[0,1,0,1]
    m=train_model(x,y)
    assert len(m.predict(x))==4
    assert "f1" in evaluate(m,x,y)
