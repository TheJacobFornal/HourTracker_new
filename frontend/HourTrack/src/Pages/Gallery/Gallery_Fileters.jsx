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
    setFilters((f) => {
      const next = {
        ...f,
        date_from: from !== undefined ? from : f.date_from,
        date_to: to !== undefined ? to : f.date_to,
      };

      // prevent re-render if nothing actually changed
      return next.date_from === f.date_from && next.date_to === f.date_to
        ? f
        : next;
    });

  const setDateSort = (v) =>
    setFilters((f) => (f.date_sort === v ? f : { ...f, date_sort: v }));

  const setSearch = (v) =>
    setFilters((f) => (f.search === v ? f : { ...f, search: v }));

  return (
    <div className="flex items-center gap-[15px] mb-4">
      <Status value={filters.status} onChange={setStatus} />
      <Leader value={filters.leader} onChange={setLeader} />
      <DateRange
        value={{ from: filters.date_from, to: filters.date_to }}
        sortOrder={filters.date_sort}
        onChange={setDateRange}
        onSortChange={setDateSort}
      />

      <Search
        value={filters.search}
        onChange={setSearch}
        onSubmit={setSearch}
      />
    </div>
  );
}
