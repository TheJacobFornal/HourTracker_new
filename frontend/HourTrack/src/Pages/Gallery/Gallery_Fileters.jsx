// Gallery_Fileters.jsx (controlled; no useEffect here)
import React from "react";
import Status from "./Filtr_Status";
import Leader from "./Filtr_Leader";
import DateRange from "./Filtr_Date";
import Search from "./Filtr_Search";

export default function GalleryFilters({ filters, setFilters }) {
  const setStatus = (v) =>
    setFilters((f) => (f.status === v ? f : { ...f, status: v }));

  const setLeader = (v) =>
    setFilters((f) => (f.leader === v ? f : { ...f, leader: v }));

  const setDateRange = ({ from, to }) =>
    setFilters((f) =>
      f.date_from === from && f.date_to === to
        ? f
        : { ...f, date_from: from, date_to: to }
    );

  const setSearch = (v) =>
    setFilters((f) => (f.search === v ? f : { ...f, search: v }));

  return (
    <div className="flex items-center gap-[15px] mb-4">
      <Status value={filters.status} onChange={setStatus} />
      <Leader value={filters.leader} onChange={setLeader} />
      <DateRange
        value={{ from: filters.date_from, to: filters.date_to }}
        onChange={setDateRange}
      />
      <Search
        value={filters.search}
        onChange={setSearch}
        onSubmit={setSearch}
      />
    </div>
  );
}
