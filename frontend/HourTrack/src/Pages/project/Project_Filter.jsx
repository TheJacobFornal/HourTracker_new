// SomePage.jsx (or ProjectPage.jsx)
import React, { useState } from "react";
import DateRange from "../Gallery/Filtr_Date"; // adjust path as needed

export default function Filtr(dateFrom, dateTo) {
  const [dates, setDates] = useState({ from: dateFrom, to: dateTo });

  // DateRange calls onChange({ from, to }) when both dates are valid (or {from:null,to:null} on clear)
  return (
    <div>
      <DateRange value={dates} onChange={setDates} />
    </div>
  );
}
