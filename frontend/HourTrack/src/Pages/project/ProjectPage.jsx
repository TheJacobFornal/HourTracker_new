// ProjectPage.jsx
import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import ProjectHeader from "./Project_Header";
import ProjectFiltr from "./Project_Filters";
import { API_ENDPOINTS } from "../../config/api";
import ActivitiesList from "./ActivitiesList";
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
        const normalizedActivities = (() => {
          if (Array.isArray(payload)) {
            if (
              payload.length === 2 &&
              Array.isArray(payload[0]) &&
              typeof payload[1] === "number"
            ) {
              activitiesStore.meta = { total: payload[1] };
              return payload[0];
            }
            return payload;
          }
          if (payload && Array.isArray(payload.activities)) {
            activitiesStore.meta = {
              total: payload.total ?? payload.activities.length,
            };
            return payload.activities;
          }
          return [];
        })();
        setActivities(normalizedActivities);
        activitiesStore.last = normalizedActivities; // make available to other modules
      } catch (e) {
        if (e.name !== "AbortError") setErr(e);
      } finally {
        setLoading(false);
      }
    })();
    return () => ac.abort();
  }, [projectId, dates.from, dates.to]);

  useEffect(() => {
    console.log("activities state updated:", activities);
  }, [activities]);

  return (
    <div className="Project_main">
      <ProjectHeader
        projectId={projectId}
        dateFrom={dates.from}
        dateTo={dates.to}
      />

      <ProjectFiltr filters={dates} setFilters={setDates} />

      {!loading && !err && <ActivitiesList data={activities} />}
    </div>
  );
}
