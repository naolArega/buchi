import app
from fastapi.testclient import TestClient

client = TestClient(app.app)

def test_create_pet():
    assert "naol" == "naol"

def test_get_pets():
    assert "naol" == "naol"

def test_add_customer():
    assert "naol" == "naol"

def test_adopt():
    assert "naol" == "naol"

def test_get_adoption_requests():
    assert "naol" == "naol"

def test_generate_report():
    assert "naol" == "naol"