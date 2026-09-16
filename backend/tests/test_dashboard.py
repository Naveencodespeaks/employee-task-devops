def test_dashboard_counts(client):
    emp_resp = client.post(
        "/api/employees",
        json={"name": "Dash User", "email": "dash@example.com", "department": "Engineering"},
    )
    employee_id = emp_resp.json()["id"]

    client.post("/api/tasks", json={"title": "T1", "employee_id": employee_id})
    t2 = client.post("/api/tasks", json={"title": "T2", "employee_id": employee_id}).json()
    client.put(f"/api/tasks/{t2['id']}", json={"status": "COMPLETED"})

    response = client.get("/api/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body["total_employees"] == 1
    assert body["total_tasks"] == 2
    assert body["todo_tasks"] == 1
    assert body["completed_tasks"] == 1
