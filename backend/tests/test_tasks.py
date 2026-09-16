def _create_employee(client):
    resp = client.post(
        "/api/employees",
        json={"name": "Task Owner", "email": "owner@example.com", "department": "Engineering"},
    )
    return resp.json()["id"]


def test_create_task(client):
    employee_id = _create_employee(client)
    response = client.post(
        "/api/tasks",
        json={"title": "Write tests", "description": "Add pytest coverage", "employee_id": employee_id},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "TODO"


def test_create_task_invalid_employee(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Orphan task", "employee_id": 9999},
    )
    assert response.status_code == 400


def test_list_and_get_task(client):
    employee_id = _create_employee(client)
    create_resp = client.post(
        "/api/tasks",
        json={"title": "Deploy service", "employee_id": employee_id},
    )
    task_id = create_resp.json()["id"]

    list_resp = client.get("/api/tasks")
    assert any(t["id"] == task_id for t in list_resp.json())

    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 200


def test_update_task_status(client):
    employee_id = _create_employee(client)
    create_resp = client.post(
        "/api/tasks",
        json={"title": "Ship feature", "employee_id": employee_id},
    )
    task_id = create_resp.json()["id"]

    update_resp = client.put(f"/api/tasks/{task_id}", json={"status": "COMPLETED"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "COMPLETED"
