// ProjectPage.jsx
import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import ProjectHeader from "./Project_Header";
import ProjectFiltr from "./Project_Filter";
import ActivitiesList from "./ActivitiesList";
const API_URL = "http://127.0.0.1:5000/api/project/activities_details";

// Simple module-level store other modules can import & read
export const activitiesStore = { last: null };

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
        const data = await res.json();
        console.log("Activities", data);
        setActivities(data);
        console.log("Activities", activities);
        activitiesStore.last = data; // make available to other modules
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
    <div className="max-w-[900px] mx-auto p-5">
      <ProjectHeader
        projectId={projectId}
        dateFrom={dates.from}
        dateTo={dates.to}
      />

      <ProjectFiltr value={dates} onChange={setDates} />

      {!loading && !err && <ActivitiesList data={activities} />}
    </div>
  );
}
