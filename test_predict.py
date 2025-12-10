from app import app

def test_predict_ok():
    client = app.test_client()
    inst = [[[0]*28 for _ in range(28)]]
    r = client.post('/predict', json={'instances': inst})
    assert r.status_code == 200
    j = r.get_json()
    assert 'predictions' in j
