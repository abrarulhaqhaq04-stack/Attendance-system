from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_checkin_twice_is_blocked():
    emp = client.post("/employees", params={"name": "Ali"}).json()
    assert client.post(f"/check-in/{emp['id']}").status_code == 200
    assert client.post(f"/check-in/{emp['id']}").status_code == 400

def test_frontend_page():
    response = client.get("/app")
    assert response.status_code == 200
