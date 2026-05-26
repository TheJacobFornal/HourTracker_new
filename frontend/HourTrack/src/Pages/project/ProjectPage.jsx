// ProjectPage.jsx
import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import ProjectHeader from "./Project_Header";
import ProjectFiltr from "./Project_Filters";
import { API_ENDPOINTS } from "../../config/api";
import ActivitiesList from "./ActivitiesList";
import User_Summary from "./Project_User_Sumarry";
import Project_Export from "./Project_Export";

const API_URL = API_ENDPOINTS.projectActivities;

// Simple module-level store other modules can import & read
export const activitiesStore = { last: null, meta: null };

export default function ProjectPage() {
  const { projectId } = useParams();
  const [sp, setSp] = useSearchParams();

  const [dates, setDates] = useState(() => ({
    from: sp.get("date_from") ?? null,
    to: sp.get("date_to") ?? null,
  }));

  useEffect(() => {
    const next = new URLSearchParams(sp);
    next.delete("date_from");
    next.delete("date_to");
    setSp(next, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps

    console.log("loaded data: ", dates);
  }, []);

  const [activities, setActivities] = useState([]);
  const [usersSummary, setUsersSummary] = useState([]);
  const [loading, setLoading] = useState(false);
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
            date_from: dates.from,
            date_to: dates.to,
          }),
          signal: ac.signal,
        });
        if (!res.ok) {
          const text = await res.text().catch(() => "");
          throw new Error(`HTTP ${res.status} ${text}`);
        }
        const payload = await res.json();
        console.log("Activities raw", payload);

        let activitiesData = [];
        let usersSummaryData = [];

        if (Array.isArray(payload)) {
          // Assuming the payload matches the structure you showed.
          if (payload.length === 2) {
            const activitiesPart = Array.isArray(payload[0]) ? payload[0] : [];
            const usersSummaryPart = Array.isArray(payload[1])
              ? payload[1]
              : [];

            // If needed, you can handle meta info here.
            if (payload[1] && typeof payload[1] === "number") {
              activitiesStore.meta = { total: payload[1] };
            } else if (payload[1] && payload[1].total) {
              activitiesStore.meta = { total: payload[1].total };
            }

            activitiesData = activitiesPart;
            usersSummaryData = usersSummaryPart;
          } else {
            // Fallback if it doesn't match the expected structure
            activitiesData = payload;
          }
        } else if (payload && Array.isArray(payload.activities)) {
          activitiesStore.meta = {
            total: payload.total ?? payload.activities.length,
          };
          activitiesData = payload.activities;
        }

        setActivities(activitiesData);
        setUsersSummary(usersSummaryData);
        activitiesStore.last = activitiesData; // make available to other modules
      } catch (e) {
        if (e.name !== "AbortError") setErr(e);
      } finally {
        setLoading(false);
      }
    })();

    return () => ac.abort();
  }, [projectId, dates.from, dates.to]);

  return (
    <div className="Project_main">
      <ProjectHeader
        projectId={projectId}
        dateFrom={dates.from}
        dateTo={dates.to}
      />

      <ProjectFiltr filters={dates} setFilters={setDates} />

      {!loading && !err && <ActivitiesList data={activities} />}

      <div
        style={{
          margin: "50px 0",
          height: "4px",
          width: "1100px",
          backgroundColor: "#0898f2ff",
          borderRadius: "6px",
          boxShadow: "0 2px 6px rgba(8, 152, 242, 0.4)",
        }}
      />

      {!loading && !err && <User_Summary data={usersSummary} />}

      {!loading && !err && <Project_Export projectId={projectId} />}
    </div>
  );
}
