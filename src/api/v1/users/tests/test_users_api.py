from uuid import uuid4


def _make_user_payload():
    suffix = uuid4().hex[:8]
    username = f"User{suffix}"
    return {
        "username": username,
        "email": f"{username.lower()}@example.com",
        "password": "Testpass1",
        "first_name": "Test",
        "last_name": "User",
        "birthdate": "1990-01-01",
    }


def test_register_user_success(client):
    payload = _make_user_payload()

    response = client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"].lower()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data


def test_login_user_success(client):
    payload = _make_user_payload()

    register_response = client.post("/api/v1/users/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={"username": payload["username"], "password": payload["password"]},
    )

    assert login_response.status_code == 200
    data = login_response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_user_invalid_credentials(client):
    payload = _make_user_payload()

    register_response = client.post("/api/v1/users/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        json={"username": payload["username"], "password": "Wrongpass1"},
    )

    assert login_response.status_code == 401
    data = login_response.json()
    assert data["error"] == "InvalidCredentialsError"
