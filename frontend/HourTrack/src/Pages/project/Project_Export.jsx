import React, { useState } from "react";
import "./Project_Style.css";
import { API_ENDPOINTS } from "../../config/api";

export default function Project_Export({ projectId }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = API_ENDPOINTS.exportExcel; // e.g., "http://127.0.0.1:8000/api/project/export_excel"

  const handleExport = async () => {
    try {
      setLoading(true);
      setMessage("");

      // POST request with project_name in JSON body
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_name: projectId }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
      }

      // Convert response to Blob for file download
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      // Trigger download using a temporary anchor
      const a = document.createElement("a");
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, "0"); // Months are 0-based
      const day = String(now.getDate()).padStart(2, "0");
      const dateStr = `${year}-${month}-${day}`;

      // Build filename
      const filename = `${projectId}_${dateStr}_HourTracker.xlsx`;
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setMessage(`✅ Excel pobrany: ${filename}`);
    } catch (err) {
      console.error("Export error:", err);
      setMessage(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="export-row">
      <button
        className="export-button"
        onClick={handleExport}
        disabled={loading}
      >
        {loading ? "Exporting..." : "Export do Excel"}
      </button>

      {message && <span className="export-message">{message}</span>}
    </div>
  );
}
