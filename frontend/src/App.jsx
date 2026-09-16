import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import Employees from "./pages/Employees.jsx";
import Tasks from "./pages/Tasks.jsx";

export default function App() {
  return (
    <div className="app-shell">
      <nav className="top-nav">
        <Link to="/">Dashboard</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/tasks">Tasks</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/tasks" element={<Tasks />} />
      </Routes>
    </div>
  );
}
