import { useEffect, useState } from "react";
import { api } from "../api/client.js";

const EMPTY_FORM = { name: "", email: "", department: "" };

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    api
      .listEmployees()
      .then(setEmployees)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.name || !form.email || !form.department) {
      setError("All fields are required.");
      return;
    }

    try {
      if (editingId) {
        await api.updateEmployee(editingId, form);
      } else {
        await api.createEmployee(form);
      }
      setForm(EMPTY_FORM);
      setEditingId(null);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (employee) => {
    setEditingId(employee.id);
    setForm({ name: employee.name, email: employee.email, department: employee.department });
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteEmployee(id);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Employees</h1>
      {error && <div className="error-banner">{error}</div>}

      <form className="inline-form" onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
        <input name="department" placeholder="Department" value={form.department} onChange={handleChange} />
        <button type="submit">{editingId ? "Update" : "Add Employee"}</button>
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setForm(EMPTY_FORM);
            }}
          >
            Cancel
          </button>
        )}
      </form>

      {loading ? (
        <p>Loading employees...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td>{emp.name}</td>
                <td>{emp.email}</td>
                <td>{emp.department}</td>
                <td>
                  <button onClick={() => startEdit(emp)}>Edit</button>{" "}
                  <button className="danger" onClick={() => handleDelete(emp.id)}>
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
