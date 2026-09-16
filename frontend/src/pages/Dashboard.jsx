import { useEffect, useState } from "react";
import { api } from "../api/client.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getDashboard()
      .then(setStats)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <div className="error-banner">Failed to load dashboard: {error}</div>;

  const cards = [
    { label: "Total Employees", value: stats.total_employees },
    { label: "Total Tasks", value: stats.total_tasks },
    { label: "To Do", value: stats.todo_tasks },
    { label: "In Progress", value: stats.in_progress_tasks },
    { label: "Completed", value: stats.completed_tasks },
  ];

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="stat-grid">
        {cards.map((c) => (
          <div className="stat-card" key={c.label}>
            <div className="value">{c.value}</div>
            <div>{c.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
