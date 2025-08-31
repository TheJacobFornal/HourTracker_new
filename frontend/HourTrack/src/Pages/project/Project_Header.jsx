// Project_Header.jsx
import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import "./Project_Style.css";

const API_URL = "http://127.0.0.1:5000/api/project/header_info";

export default function ProjectHeader() {
  const { projectId } = useParams();
  const [sp] = useSearchParams();
  const urlDateFrom = sp.get("date_from") || null;
  const urlDateTo = sp.get("date_to") || null;

  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    const ac = new AbortController();
    (async () => {
      try {
        setLoading(true);
        setErr(null);
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            project_name: projectId,
            date_from: urlDateFrom,
            date_to: urlDateTo,
          }),
          signal: ac.signal,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        // accept either an object or a 1-element array
        setInfo(Array.isArray(json) ? json[0] : json);
      } catch (e) {
        if (e.name !== "AbortError") setErr(e);
      } finally {
        setLoading(false);
      }
    })();
    return () => ac.abort();
  }, [projectId, urlDateFrom, urlDateTo]);

  const dateFrom = info?.dateFrom || urlDateFrom;
  const dateTo = info?.dateTo || urlDateTo;
  const leader = info?.leader;
  const status = info?.status;

  return (
    <header className="ProjectHeader">
      {/* add ProjectHeader--fullbleed if you want full page width */}
      <div className="Header_Left_Div">
        <h1 className="text-3xl font-bold mb-2">Project: {projectId}</h1>
      </div>

      <div className="Header_Right_Div">
        <p>
          {dateFrom || dateTo ? (
            <>
              Od {dateFrom ?? "—"} do {dateTo ?? "—"}
            </>
          ) : (
            <span className="text-gray-500">Brak zakresu dat</span>
          )}
        </p>
        <p>Project Leader: {loading ? "…" : leader ?? "—"}</p>
        <p>Status: {loading ? "…" : status ?? "—"}</p>
        {err && (
          <p className="text-red-600 text-sm">
            Błąd: {String(err.message || err)}
          </p>
        )}
      </div>
    </header>
  );
}
