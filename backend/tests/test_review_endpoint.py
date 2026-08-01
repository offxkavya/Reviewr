from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_current_user

class MockUser:
    id = 1
    github_id = "12345"
    username = "testuser"
    email = "test@example.com"

app.dependency_overrides[get_current_user] = lambda: MockUser()

client = TestClient(app)

def test_review_endpoint_success():
    payload = {
        "code": "print('hello world')",
        "language": "python"
    }
    response = client.post("/api/review", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "comments" in data
    assert len(data["comments"]) > 0

def test_review_endpoint_validation_error():
    payload = {
        "code": "   ",
        "language": "python"
    }
    response = client.post("/api/review", json=payload)
    assert response.status_code == 422  # Pydantic validation error returns 422
