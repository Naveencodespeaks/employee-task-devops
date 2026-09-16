def test_create_employee(client):
    response = client.post(
        "/api/employees",
        json={"name": "Jane Doe", "email": "jane@example.com", "department": "Engineering"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Jane Doe"
    assert body["email"] == "jane@example.com"
    assert "id" in body


def test_list_and_get_employee(client):
    create_resp = client.post(
        "/api/employees",
        json={"name": "Alex Kim", "email": "alex@example.com", "department": "HR"},
    )
    employee_id = create_resp.json()["id"]

    list_resp = client.get("/api/employees")
    assert list_resp.status_code == 200
    assert any(e["id"] == employee_id for e in list_resp.json())

    get_resp = client.get(f"/api/employees/{employee_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "alex@example.com"


def test_get_employee_not_found(client):
    response = client.get("/api/employees/9999")
    assert response.status_code == 404
