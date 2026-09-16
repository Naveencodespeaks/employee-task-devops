import { useEffect, useState } from "react";
import { api } from "../api/client.js";

const STATUSES = ["TODO", "IN_PROGRESS", "COMPLETED"];
const EMPTY_FORM = { title: "", description: "", employee_id: "" };

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    Promise.all([api.listTasks(), api.listEmployees()])
      .then(([taskData, employeeData]) => {
        setTasks(taskData);
        setEmployees(employeeData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const employeeName = (id) => employees.find((e) => e.id === id)?.name || `#${id}`;

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.title || !form.employee_id) {
      setError("Title and assigned employee are required.");
      return;
    }

    try {
      await api.createTask({ ...form, employee_id: Number(form.employee_id) });
      setForm(EMPTY_FORM);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleStatusChange = async (task, status) => {
    try {
      await api.updateTask(task.id, { status });
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteTask(id);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Tasks</h1>
      {error && <div className="error-banner">{error}</div>}

      <form className="inline-form" onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} />
        <input name="description" placeholder="Description" value={form.description} onChange={handleChange} />
        <select name="employee_id" value={form.employee_id} onChange={handleChange}>
          <option value="">Assign to...</option>
          {employees.map((emp) => (
            <option key={emp.id} value={emp.id}>
              {emp.name}
            </option>
          ))}
        </select>
        <button type="submit">Add Task</button>
      </form>

      {loading ? (
        <p>Loading tasks...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Assigned To</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id}>
                <td>{task.title}</td>
                <td>{employeeName(task.employee_id)}</td>
                <td>
                  <select value={task.status} onChange={(e) => handleStatusChange(task, e.target.value)}>
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <button className="danger" onClick={() => handleDelete(task.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
