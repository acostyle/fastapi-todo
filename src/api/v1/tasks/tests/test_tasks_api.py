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


def _register_user(client):
    payload = _make_user_payload()
    response = client.post("/api/v1/users/register", json=payload)
    assert response.status_code == 201
    return payload, response.json()


def _login_user(client, username: str, password: str) -> str:
    response = client.post(
        "/api/v1/users/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_tasks_require_auth(client):
    list_response = client.get("/api/v1/tasks/")
    assert list_response.status_code == 401

    create_response = client.post("/api/v1/tasks/", json={"title": "Test"})
    assert create_response.status_code == 401

    update_response = client.patch(
        f"/api/v1/tasks/{uuid4()}",
        json={"title": "Updated"},
    )
    assert update_response.status_code == 401

    invalid_token_response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert invalid_token_response.status_code == 401


def test_create_and_list_tasks(client):
    payload, _ = _register_user(client)
    token = _login_user(client, payload["username"], payload["password"])
    headers = _auth_headers(token)

    empty_list = client.get("/api/v1/tasks/", headers=headers)
    assert empty_list.status_code == 200
    assert empty_list.json() == []

    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "First task", "description": "Details"},
        headers=headers,
    )
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "First task"
    assert created_task["description"] == "Details"
    assert created_task["is_done"] is False

    list_response = client.get("/api/v1/tasks/", headers=headers)
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created_task["id"]


def test_update_task_and_access_control(client):
    payload_a, _ = _register_user(client)
    token_a = _login_user(client, payload_a["username"], payload_a["password"])
    headers_a = _auth_headers(token_a)

    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Owner task"},
        headers=headers_a,
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    payload_b, _ = _register_user(client)
    token_b = _login_user(client, payload_b["username"], payload_b["password"])
    headers_b = _auth_headers(token_b)

    other_user_list = client.get("/api/v1/tasks/", headers=headers_b)
    assert other_user_list.status_code == 200
    assert other_user_list.json() == []

    forbidden_update = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=headers_b,
    )
    assert forbidden_update.status_code == 404
    assert forbidden_update.json()["error"] == "TaskNotFoundError"

    update_response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"is_done": True, "title": "Updated title"},
        headers=headers_a,
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == task_id
    assert updated["is_done"] is True
    assert updated["title"] == "Updated title"
