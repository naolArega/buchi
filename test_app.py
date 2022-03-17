from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_pet():
    response = client.post("/pet/create_pet", json={
        "type": "Cat",
        "gender": "male",
        "size": "medium",
        "age": 5,
        "photos": [
            {
                "data": "YWJlYmVuYW9sYXNkYQ==",
                "extension": "png"
            }
        ],
        "good_with_children": True
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_pets():
    response =  client.get("/pet/get_pets?limit=10")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_add_customer():
    response = client.post("/customer/add_customer", json={
        "name": "Jane Doe",
        "phone": "0911121314"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_adopt():
    response = client.post("/adoption/adopt", json={        
        "customer_id": "6231bdaf6d92a353a4b905c2",
        "pet_id": "6231bdd56d92a353a4b905c3"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_adoption_requests():
    response = client.get("/adoption/get_adoption_requests?from_date=2022-02-05&to_date=2022-04-12")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_generate_report():
    response = client.post("/report/generate_report", json={
        "from_date": "2022-03-15",
        "to_date": "2022-03-19"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"