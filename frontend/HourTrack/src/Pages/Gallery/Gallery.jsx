// Gallery.jsx
import React, { useEffect, useState } from "react";
import GalleryHeader from "./Gallery_Header";
import GalleryFilters from "./Gallery_Fileters";
import GalleryGrid from "./Gallery_Grid";
import "./Gallery.css";

const API_URL = "http://127.0.0.1:5000/api/projects/search";

function useDebounced(value, delay = 300) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return v;
}

export default function Gallery() {
  const [projectList, setProjectList] = useState([]);
  const [filters, setFilters] = useState({
    users: [],
    status: "ALL",
    leader: "ALL",
    date_from: null,
    date_to: null,
    search: "",
  });

  const debouncedFilters = useDebounced(filters, 300);

  useEffect(() => {
    const ac = new AbortController();
    (async () => {
      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(debouncedFilters),
          signal: ac.signal,
        });
        if (!res.ok) return;
        const data = await res.json();
        setProjectList(data);
      } catch (e) {
        if (e.name !== "AbortError") console.error("API error:", e);
      }
    })();
    return () => ac.abort();
  }, [debouncedFilters]);

  return (
    <div className="max-w-[1900px] w-full mx-auto px-5">
      <div className="HeaderDiv">
        <GalleryHeader />
      </div>

      <div className="FilterDiv">
        <GalleryFilters filters={filters} setFilters={setFilters} />
      </div>

      <div className="GridDiv">
        <GalleryGrid projects={projectList} filters={filters} />
      </div>
    </div>
  );
}
