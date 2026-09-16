// Small fetch wrapper. Base URL is injected at build time via Vite env vars
// so the same built bundle can be re-pointed at a different backend by
// just changing VITE_API_BASE_URL when building the Docker image.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // response had no JSON body; keep statusText
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  listEmployees: () => request("/api/employees"),
  createEmployee: (data) => request("/api/employees", { method: "POST", body: JSON.stringify(data) }),
  updateEmployee: (id, data) => request(`/api/employees/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteEmployee: (id) => request(`/api/employees/${id}`, { method: "DELETE" }),

  listTasks: () => request("/api/tasks"),
  createTask: (data) => request("/api/tasks", { method: "POST", body: JSON.stringify(data) }),
  updateTask: (id, data) => request(`/api/tasks/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteTask: (id) => request(`/api/tasks/${id}`, { method: "DELETE" }),

  getDashboard: () => request("/api/dashboard"),
};
