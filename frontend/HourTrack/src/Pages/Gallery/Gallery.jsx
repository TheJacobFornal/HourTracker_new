// Gallery.jsx
import React, { useEffect, useState, useRef } from "react";
import GalleryHeader from "./Gallery_Header";
import GalleryFilters from "./Gallery_Fileters";
import GalleryGrid from "./Gallery_Grid";
import { API_ENDPOINTS, API_BASE_URL } from "../../config/api";
import "./Gallery.css";

const API_URL = API_ENDPOINTS.projectsSearch;
const API_PORT = (() => {
  try {
    const url = new URL(API_BASE_URL);
    if (url.port) return url.port;
    return url.protocol === "https:" ? "443" : "80";
  } catch (e) {
    console.error("Failed to parse API base URL", e);
    return "unknown";
  }
})();

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
  const [result_count, setResultCount] = useState(0);
  const [apiReady, setApiReady] = useState(null);
  const [filters, setFilters] = useState({
    users: [],
    status: "ALL",
    leader: "ALL",
    date_from: null,
    date_to: null,
    date_sort: "begin",
    search: "",
    page: 1, // add page
    page_size: 51, // add page_size
  });
  const [loading, setLoading] = useState(true); // set initial loading to true
  const isFirstRender = useRef(true);

  // Reset page to 1 when filters (except page/page_size) change, but skip on first render
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    setFilters((f) => ({ ...f, page: 1 }));
    // eslint-disable-next-line
  }, [
    filters.status,
    filters.leader,
    filters.date_from,
    filters.date_to,
    filters.date_sort,
    filters.search,
  ]);

  useEffect(() => {
    if (filters.date_from || filters.date_to) {
      console.log("Date range changed:", {
        from: filters.date_from,
        to: filters.date_to,
      });
    }
  }, [filters.date_from, filters.date_to]);

  const debouncedFilters = useDebounced(filters, 300);

  useEffect(() => {
    setLoading(true);
    setApiReady(null);
    const ac = new AbortController();
    (async () => {
      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(debouncedFilters),
          signal: ac.signal,
        });
        if (!res.ok) {
          setApiReady(false);
          return;
        }
        const data = await res.json();
        setProjectList(data.projects); // list of projects
        setResultCount(data.record_counter); // total matching rows
        setApiReady(true);
        window.scrollTo({ top: 0, behavior: "smooth" }); // scroll to top after loading
      } catch (e) {
        if (e.name === "AbortError") return;
        console.error("API error:", e);
        setApiReady(false);
      } finally {
        setLoading(false);
      }
    })();
    return () => ac.abort();
  }, [debouncedFilters]);

  // Pagination handler
  const handlePageChange = (newPage) => {
    setFilters((f) => ({ ...f, page: newPage }));
  };

  return (
    <div className="main_box">
      <h1></h1>
      <div className="HeaderDiv">
        <GalleryHeader result_count={result_count} />
      </div>

      <div className="FilterDiv">
        <GalleryFilters filters={filters} setFilters={setFilters} />
      </div>

      <div className="GridDiv">
        {loading ? (
          <div
            className="flex items-center justify-center"
            style={{ minHeight: "300px" }}
          >
            <span
              style={{
                fontSize: "2.5rem",
                color: "#888",
                fontWeight: 700,
                letterSpacing: "1px",
              }}
            >
              Loading projects...
            </span>
          </div>
        ) : projectList.length === 0 ? (
          <div
            className="flex items-center justify-center"
            style={{ minHeight: "300px" }}
          >
            <span
              style={{
                fontSize: "2.5rem",
                color: "#888",
                fontWeight: 700,
                letterSpacing: "1px",
              }}
            >
              brak projektów
            </span>
          </div>
        ) : (
          <GalleryGrid
            projects={projectList}
            filters={filters}
            totalCount={result_count}
            onPageChange={handlePageChange}
          />
        )}
      </div>
    </div>
  );
}
