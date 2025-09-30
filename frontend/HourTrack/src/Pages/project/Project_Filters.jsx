// Gallery_Fileters.jsx (controlled; no useEffect here)
import React from "react";
import DateRange from "./Filtr_Date_Project";
import "./Project_Style.css";

export default function ProjectFilters({ filters = {}, setFilters }) {
  const setDateRange = ({ from, to }) =>
    setFilters((f) => {
      if (f.from === from && f.to === to) return f;
      return { ...f, from, to };
    });

  return (
    <div className="filters-container">
      <DateRange
        value={{ from: filters.from, to: filters.to }}
        onChange={setDateRange}
      />
    </div>
  );
}
