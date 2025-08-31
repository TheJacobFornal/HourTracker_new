// ProjectCard.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Gallery.css";

const asYMD = (v) => {
  if (!v) return "";
  if (typeof v === "string") return v; // already "YYYY-MM-DD"
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  return String(v);
};

const buildDateQuery = (filters) => {
  if (!filters) return "";
  const params = new URLSearchParams();

  const from = asYMD(filters.date_from);
  const to = asYMD(filters.date_to);

  if (from) params.set("date_from", from);
  if (to) params.set("date_to", to);

  const qs = params.toString();
  return qs ? `?${qs}` : "";
};

const ProjectCard = ({ id, hours, user, dateRange, filters }) => (
  <Link
    to={`/projects/${encodeURIComponent(id)}${buildDateQuery(filters)}`}
    className="block no-underline"
    style={{ textDecoration: "none", color: "inherit" }}
  >
    <div style={{ ...styles.card, cursor: "pointer" }}>
      <div className="CardMain" style={styles.header}>
        <span style={styles.icon}>🔻</span>
        <strong>{id}</strong>
        <span style={{ marginLeft: "auto", fontWeight: "bold" }}>
          {hours} H
        </span>
      </div>
      <hr />
      <div style={styles.body}>
        <p style={{ fontWeight: 600, margin: "4px 0" }}>{user}</p>
        <p style={{ color: "#655", fontSize: 15 }}>{dateRange}</p>
      </div>
    </div>
  </Link>
);

const styles = {
  card: {
    border: "1.5px solid #ccc",
    borderRadius: 8,
    padding: 15,
    width: 350,
    boxSizing: "border-box",
  },
  header: { display: "flex", alignItems: "center", fontSize: 19 },
  icon: { color: "orange", marginRight: 8 },
  body: { marginTop: 10 },
};

export default ProjectCard;
