// ProjectCard.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Gallery.css";
import calendarIcon from "../../assets/calendar.png";
import leaderIcon from "../../assets/leader.png";

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
        <strong style={styles.id} title={id}>{id}</strong>
        <span style={styles.hours}>
          {hours} H
        </span>
      </div>
      <hr />
      <div style={styles.body}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <img
            src={calendarIcon}
            alt="calendar"
            style={{
              width: 22,
              height: 22,
              marginRight: 6,
            }}
          />
          <p
            style={{
              fontWeight: 600,
              margin: 0,
            }}
          >
            {dateRange}
          </p>
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            margin: "4px 0",
          }}
        >
          <img
            src={leaderIcon}
            alt="leader"
            style={{ width: 22, height: 22, marginRight: 3 }}
          />
          <p style={{ fontWeight: 600, margin: 0 }}>{user}</p>
        </div>
      </div>
    </div>
  </Link>
);

const styles = {
  card: {
    border: "1.5px solid #afafafff",
    borderRadius: 16,
    padding: 14,
    width: 350,
    Height: 100,
    boxSizing: "border-box",
    background: "#f9f9fb",
    boxShadow: "0 4px 16px 0 rgba(45, 45, 45, 0.13)",
    transition:
      "box-shadow 0.18s, border-color 0.18s, transform 0.18s, background 0.18s",
    margin: "3px 0",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    gap: 3,
    cursor: "pointer",
  },
  header: { display: "flex", alignItems: "center", fontSize: 19 },
  icon: { color: "orange", marginRight: 8 },
  id: { flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", fontWeight: 700 },
  hours: { marginLeft: "auto", fontWeight: "bold", whiteSpace: "nowrap", flexShrink: 0 },
  body: { marginTop: 10 },
};

export default ProjectCard;
